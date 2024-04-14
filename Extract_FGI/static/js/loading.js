//如果把这段注释掉，会一直停留在加载的页面上
$(window).load(function(){
         $(".loading").fadeOut()
        })

/**这个是调整窗口大小的函数，如果注释掉，整个页面布局会乱掉**/
$(document).ready(
function()
    {
        var whei=$(window).width()
        $("html").css({fontSize:whei/20})

        $(window).resize(
        function()
            {
            var whei=$(window).width()
            $("html").css({fontSize:whei/20})
            }
        );

	}
);