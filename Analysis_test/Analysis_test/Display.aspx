<html>
    <head>
        <title>Display</title>
        <script src="js/jquery.min.js"></script>
        <script src="echarts.min.js"></script>
        <script>
            $(function () {
                $("#page2").click(function () {
                    $("#right").html("<iframe src=\"Bayes_distribution.html\" width=\"100%\" height=\"80%\"></iframe>");
                });
                $("#page3").click(function () {
                    $("#right").html("<iframe src=\"browser_webpages_top_10.html\" width=\"100%\" height=\"80%\"></iframe>");
                });
                $("#page1").click(function () {
                    $("#right").html("<iframe src=\"initial_URL_distribution.html\" width=\"100%\" height=\"80%\"></iframe>");
                });
                $("#page4").click(function () {
                    $("#right").html("<iframe src=\"proportion.html\" width=\"100%\" height=\"80%\"></iframe>");
                });
                $("#page5").click(function () {
                    $("#right").html("<iframe src=\"personal_hobby.html\" width=\"100%\" height=\"80%\"></iframe>");
                });
            });
        </script>
        <style>
            .left{
                float:left;
                width:18%;
            }
            .right{
                float:right;
                width:70%;
            }
            .left button{
                width:50%;
                height:38px;
                background-color:#eee;
                border:1px solid #fff;
                border-radius:4px;
                margin:10px 20px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <center><h1>Display</h1></center>
        </div>
        <div class="left">
            <button id="page1">Initial_URL_distribution</button><br />
            <button id="page2">Bayes_distribution</button><br />
            <button id="page3">top_10</button><br />
            <button id="page4">Total Proportion</button><br />
            <button id="page5">Personal hobby</button><br />
        </div>
        <div class="right" id="right">
            <iframe id="rightframe" src="introduction.html" width="100%" height="80%"></iframe>
        </div>
    </body>
</html>