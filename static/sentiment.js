/*var btn = document.getElementById('submit');
var tpl = _.template(document.getElementById('templ-results').innerHTML);
btn.addEventListener("click", function(event) {
	var txt = document.getElementById('txt').value;
	$.post('web/text/', {"txt": txt}, function (data) {		
		document.getElementById('result').innerHTML = tpl(data);
	});
});
*/
var btn2 = document.getElementById('submit_sentiment');
var tp2 = _.template(document.getElementById('sentiment-results').innerHTML);
btn2.addEventListener("click", function(event) {
        var txt = document.getElementById('txt').value;
        $.post('text/', {"txt": txt}, function (data) {
                document.getElementById('sentiment_result').innerHTML = tp2(data);
        });
});
