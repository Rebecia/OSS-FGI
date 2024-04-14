$(function echarts_1() {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('echart1'));

    option = {
    backgroundColor: '#00265f',         // 整个绘图区域的背景颜色
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    grid: {
        left: '0%',
        top: '0%',
		//top:'10px',
        right: '0%',
        bottom: '0%',
        //bottom: '4%',
       containLabel: true
    },
    xAxis: [{
        type: 'category',
        data: {{form.echart1.xAxis|safe}},
        // 坐标轴的线条，颜色为白色，设置为0.1的透明度
        axisLine: {
            show: true,
            lineStyle: {
                color: "rgba(255,255,255,.1)",
                width: 1,
                type: "solid"
            },
        },
        axisTick: { show: false,},
        // 坐标轴文字的颜色，设置为0.6的透明度
		axisLabel:  {
                interval: 0,
                rotate:50,
                show: true,
                splitNumber: 15,
                textStyle: {
 					color: "rgba(255,255,255,.6)",
                    fontSize: '12',},
                },}],

    yAxis: [{
        type: 'value',
        axisLabel: {
       //formatter: '{value} %'
        show:true,
         textStyle: {
                color: "rgba(255,255,255,.6)",
                fontSize: '12',
                },
        },
        axisTick: {
            show: false,
        },
        axisLine: {
            show: true,
            lineStyle: {
                color: "rgba(255,255,255,.1	)",
                width: 1,
                type: "solid"
            },
        },
        splitLine: {                            // 分割线
            lineStyle: {
               color: "rgba(255,255,255,.1)",
            }
        }
    }],
    series: [
		{
        type: 'bar',
        data: {{form.echart1.series|safe}},
        barWidth:'35%', //柱子宽度
       // barGap: 1, //柱子之间间距
        itemStyle: {
            normal: {
                color:'#2f89cf',
                opacity: 1,     // 完全不透明
				barBorderRadius: 5, // 圆柱的半径
            }
        }
    }

	]
};

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        // 可以随着窗口大小的变化自适应地改变窗口大小
        window.addEventListener("resize",function(){
            myChart.resize();
        });
    })
