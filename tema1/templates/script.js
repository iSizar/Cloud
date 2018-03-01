var settings = {
  "async": true,
  "crossDomain": true,
  "url": "https://en.wikipedia.org/w/api.php?action=query&titles=Main%20Page&prop=revisions&rvprop=content&format=json&formatversion=2",
  "method": "GET"
  
}

$.ajax(settings).done(function (response) {
  console.log(response);
});
