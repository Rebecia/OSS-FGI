import pandas as pd
from pyecharts.charts import Bar, Pie, Tab
from pyecharts.render import make_snapshot
from pyecharts.globals import CurrentConfig, NotebookType
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Bar, Pie, Grid
from pyecharts.charts import Bar
from pyecharts import options as opts
import os
import json

sodan = []
endan=[]

# Dynamic APIs：msg, ip_address
def count_messages_and_ip_addresses(data):
    msg_counts = {}
    ip_address_counts = {}

    for category, category_data in data.items():
        for entry in category_data:
            msg = entry.get('msg')
            ip_address = entry.get('ip_address')

            if msg:
                if category not in msg_counts:
                    msg_counts[category] = {}
                if msg not in msg_counts[category]:
                    msg_counts[category][msg] = 0
                msg_counts[category][msg] += 1

            if ip_address:
                if category not in ip_address_counts:
                    ip_address_counts[category] = {}
                if ip_address not in ip_address_counts[category]:
                    ip_address_counts[category][ip_address] = 0
                ip_address_counts[category][ip_address] += 1

    return msg_counts, ip_address_counts


folder_path = ' '

total_msg_counts = {}
total_ip_address_counts = {}


for root, dirs, files in os.walk(folder_path):

    for file in files:
        if file.startswith('summary') and file.endswith('.json'):
            file_path = os.path.join(root, file)

            with open(file_path, 'r') as f:
                json_data = json.load(f)

            print(file_path)
            msg_counts, ip_address_counts = count_messages_and_ip_addresses(
                json_data)

            sum_cout = 0
            net_cout = 0
            file_cout = 0
            process_cout = 0

            for category, msg_count in msg_counts.items():
                if category == 'network':
                    for msg, count in msg_count.items():
                        net_cout += count
                if category == 'files':
                    for msg, count in msg_count.items():
                        file_cout += count
                if category == 'process':
                    for msg, count in msg_count.items():
                        process_cout += count
            sum_cout = net_cout+file_cout+process_cout
            endan.append([net_cout,file_cout,process_cout,sum_cout])

            for category, msg_count in msg_counts.items():
                if category not in total_msg_counts:
                    total_msg_counts[category] = {}
                for msg, count in msg_count.items():
                    if msg not in total_msg_counts[category]:
                        total_msg_counts[category][msg] = 0
                    total_msg_counts[category][msg] += count

            for category, ip_count in ip_address_counts.items():
                if category not in total_ip_address_counts:
                    total_ip_address_counts[category] = {}
                for ip_address, count in ip_count.items():
                    if ip_address not in total_ip_address_counts[category]:
                        total_ip_address_counts[category][ip_address] = 0
                    total_ip_address_counts[category][ip_address] += count


print("Message Counts:")
for category, msg_count in total_msg_counts.items():
    print(f"\nCategory: {category}")
    for msg, count in msg_count.items():
        print(f"Message: {msg} | Count: {count}")

print("\nIP Address Counts:")
for category, ip_count in total_ip_address_counts.items():
    print(f"\nCategory: {category}")
    for ip_address, count in ip_count.items():
        print(f"IP Address: {ip_address} | Count: {count}")

# Statistical Results
if 'network' in total_msg_counts:
    network_msg_counts = total_msg_counts["network"]  
    network_msg_counts_sorted = sorted(
        network_msg_counts.items(), key=lambda x: x[1], reverse=True)
    for item in network_msg_counts_sorted:
        sodan.append(['network', item[0], item[1]])
    network_msg_names = [item[0] for item in network_msg_counts_sorted]
    network_msg_values = [item[1] for item in network_msg_counts_sorted]

if 'files' in total_msg_counts:
    file_msg_counts = total_msg_counts["files"]  
    file_msg_counts_sorted = sorted(
        file_msg_counts.items(), key=lambda x: x[1], reverse=True)
    for item in file_msg_counts_sorted:
        sodan.append(['file', item[0], item[1]])

    file_msg_names = [item[0] for item in file_msg_counts_sorted]
    file_msg_values = [item[1] for item in file_msg_counts_sorted]

if 'process' in total_msg_counts:
    system_call_msg_counts = total_msg_counts["process"]
    system_call_msg_counts_sorted = sorted(
        system_call_msg_counts.items(), key=lambda x: x[1], reverse=True)
    for item in system_call_msg_counts_sorted:
        sodan.append(['call', item[0], item[1]])
    system_call_msg_names = [item[0] for item in system_call_msg_counts_sorted]
    system_call_msg_values = [item[1] for item in system_call_msg_counts_sorted]

if 'neteork' in total_ip_address_counts:
    ip_counts = total_ip_address_counts["network"]
    ip_counts_sorted = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)
    for item in ip_counts_sorted:
        sodan.append(['ip', item[0], item[1]])

    ip_names = [item[0] for item in ip_counts_sorted]
    ip_values = [item[1] for item in ip_counts_sorted]

df = pd.DataFrame(sodan, columns=['Category', 'Name', 'count'])
writer = pd.ExcelWriter('mnpm.xlsx', engine='openpyxl')
df.to_excel(writer, sheet_name='Sheet1', index=False)
writer._save()

df = pd.DataFrame(endan, columns=['net_cout','file_cout','process_cout','sum_cout'])
writer = pd.ExcelWriter('mnpm_CDF.xlsx', engine='openpyxl')
df.to_excel(writer, sheet_name='Sheet1', index=False)
writer._save()


# # ar Chart
# bar_network = (
#     Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
#     .add_xaxis(network_msg_names)
#     .add_yaxis("Network", network_msg_values)
#     .set_global_opts(
#         title_opts=opts.TitleOpts(title="Network Message Counts"),
#         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
#         yaxis_opts=opts.AxisOpts(name="Count"),
#     )
# )

# bar_file = (
#     Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
#     .add_xaxis(file_msg_names)
#     .add_yaxis("File", file_msg_values)
#     .set_global_opts(
#         title_opts=opts.TitleOpts(title="File Message Counts"),
#         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
#         yaxis_opts=opts.AxisOpts(name="Count"),
#     )
# )

# bar_system_call = (
#     Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
#     .add_xaxis(system_call_msg_names)
#     .add_yaxis("System Call", system_call_msg_values)
#     .set_global_opts(
#         title_opts=opts.TitleOpts(title="System Call Message Counts"),
#         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
#         yaxis_opts=opts.AxisOpts(name="Count"),
#     )
# )


# bar_ip = (
#     Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
#     .add_xaxis(ip_names)
#     .add_yaxis("IP", ip_values)
#     .set_global_opts(
#         title_opts=opts.TitleOpts(title="IP Counts"),
#         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
#         yaxis_opts=opts.AxisOpts(name="Count"),
#     )
# )

# # Pie Chart
# pie_network = (
#     Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
#     .add("", [list(z) for z in zip(network_msg_names, network_msg_values)])
#     .set_global_opts(
#         title_opts=opts.TitleOpts(title="Network Message Counts"),
#         legend_opts=opts.LegendOpts(pos_left="center", orient="vertical"),
#     )
#     .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
# )

# # 创建文件类别饼图
# pie_file = (
#     Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
#     .add("", [list(z) for z in zip(file_msg_names, file_msg_values)])
#     .set_global_opts(
#         title_opts=opts.TitleOpts(title="File Message Counts"),
#         legend_opts=opts.LegendOpts(pos_left="center", orient="vertical"),
#     )
#     .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
# )

# pie_system_call = (
#     Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
#     .add("", [list(z) for z in zip(system_call_msg_names, system_call_msg_values)])
#     .set_global_opts(
#         title_opts=opts.TitleOpts(title="System Call Message Counts"),
#         legend_opts=opts.LegendOpts(pos_left="center", orient="vertical"),
#     )
#     .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
# )
# pie_ip = (
#     Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
#     .add("", [list(z) for z in zip(ip_names, ip_values)])
#     .set_global_opts(
#         title_opts=opts.TitleOpts(title="IP Counts"),
#         legend_opts=opts.LegendOpts(pos_left="center", orient="vertical"),
#     )
#     .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
# )

# # Create A Tab Page And Add Various Charts As Tabs
# tab = Tab()
# tab.add(bar_network, "Network Message Counts")
# tab.add(bar_file, "File Message Counts")
# tab.add(bar_system_call, "System Call Message Counts")
# tab.add(bar_ip, "IP Counts")
# tab.add(pie_network, "Network Message Counts (Pie)")
# tab.add(pie_file, "File Message Counts (Pie)")
# tab.add(pie_system_call, "System Call Message Counts (Pie)")
# tab.add(pie_ip, "IP Counts (Pie)")

# # Save As Html File
# tab.render("all_charts.html")
