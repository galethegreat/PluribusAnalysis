anychart.onDocumentReady(function() {
var data = {
 header: ["Player", "Number of Hands Dealt"],
 rows: [
["Bill", 9],
["MrOrange", 6],
["MrBlue", 6],
["MrWhite", 5],
["Eddie", 4],
["Budd", 4],
["MrPink", 3],
["Pluribus", 2],
["MrBlonde", 1],
["Joe", 1],
["ORen", 0],
["MrBrown", 0],
["Hattori", 0],
["Gogo", 0]
]}
var chart = anychart.column();
chart.data(data);
chart.title("Amount of A A dealt to players");
chart.container('container');
chart.draw();
});
