// addEventListener
document.getElementById("search-form").addEventListener("submit", function (e) {
  e.preventDefault(); // 防止表單跳轉和重新刷新頁面
  search(); // 調用自定義的 search 函數來處理表單提交
});

//Search
function search() {
  var resultsElement = document.getElementById("results");
  var buttonsElement = document.getElementById("buttons");

  // Clear previous results
  resultsElement.innerHTML = "";
  buttonsElement.innerHTML = "";

  // Get Form Input
  var q = document.getElementById("query").value;

  var apiKey = "AIzaSyAGw2Lgj16eu4IpoyY1U47zbiashZRy58c";
  var requestURL = `https://www.googleapis.com/youtube/v3/search?part=snippet,id&type=video&q="+
  ${q} + &key=${apiKey}`;

  fetch(requestURL)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log(data); // Console log for debugging
      var nextPageToken = data.nextPageToken;
      var prevPageToken = data.prevPageToken;

      // Dynamically create list items for each video and append to results element
      data.items.forEach((item) => {
        var output = getOutput(item); // getOutput is a function that returns HTML string
        var li = document.createElement("li");
        li.innerHTML = output;
        resultsElement.appendChild(li);
      });

      var buttons = getButtons(prevPageToken, nextPageToken); // returns HTML string for buttons
      buttonsElement.innerHTML = buttons;
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
    });
}

// Build videoo lists Output
function getOutput(item) {
  var videoId = item.id.videoId;
  var title = item.snippet.title;
  var description = item.snippet.description;
  var thumb = item.snippet.thumbnails.high.url;
  var channelTitle = item.snippet.channelTitle;
  var videoDate = item.snippet.publishedAt;

  // Build Output String
  var output =
    "<li>" +
    '<div class="list-left">' +
    '<img src="' +
    thumb +
    '">' +
    "</div>" +
    '<div class="list-right">' +
    '<h3><a class="fancybox fancybox.iframe" href="http://www.youtube.com/embed/' +
    videoId +
    '">' +
    title +
    "</a></h3>" +
    '<small>By <span class="cTitle">' +
    channelTitle +
    "</span> on " +
    videoDate +
    "</small>" +
    "<p>" +
    description +
    "</p>" +
    "</div>" +
    "</li>" +
    '<div class="clearfix"></div>' +
    "";

  return output;
}

// Build the buttons
function getButtons(prevPageToken, nextPageToken) {
  if (!prevPageToken) {
    var btnoutput =
      '<div class="button-container">' +
      '<button id="next-button" class="paging-button" data-token="' +
      nextPageToken +
      '" data-query="' +
      q +
      '"' +
      'onclick="nextPage();">Next Page</button></div>';
  } else {
    var btnoutput =
      '<div class="button-container">' +
      '<button id="prev-button" class="paging-button" data-token="' +
      prevPageToken +
      '" data-query="' +
      q +
      '"' +
      'onclick="prevPage();">Prev Page</button>' +
      '<button id="next-button" class="paging-button" data-token="' +
      nextPageToken +
      '" data-query="' +
      q +
      '"' +
      'onclick="nextPage();">Next Page</button></div>';
  }

  return btnoutput;
}

// Next Page Function
function nextPage() {
  var token = document.getElementById("next-button").getAttribute("data-token");
  //   var q = document.getElementById("query").value;

  // Clear previous results
  resultsElement.innerHTML = "";
  buttonsElement.innerHTML = "";

  // Get Form Input
  var q = document.getElementById("query").value;

  var apiKey = "AIzaSyAGw2Lgj16eu4IpoyY1U47zbiashZRy58c";
  var requestURL = `https://www.googleapis.com/youtube/v3/search?part=snippet,id&type=video&q="+
  ${q} + &key=${apiKey} + pageToken=${token}`;

  fetch(requestURL)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log(data); // Console log for debugging
      var nextPageToken = data.nextPageToken;
      var prevPageToken = data.prevPageToken;

      // Dynamically create list items for each video and append to results element
      data.items.forEach((item) => {
        var output = getOutput(item); // getOutput is a function that returns HTML string
        var li = document.createElement("li");
        li.innerHTML = output;
        resultsElement.appendChild(li);
      });

      var buttons = getButtons(prevPageToken, nextPageToken); // returns HTML string for buttons
      buttonsElement.innerHTML = buttons;
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
    });
}

// Prev Page Function
function nextPage() {
  var token = document.getElementById("prev-button").getAttribute("data-token");
  //   var q = document.getElementById("query").value;

  // Clear previous results
  resultsElement.innerHTML = "";
  buttonsElement.innerHTML = "";

  // Get Form Input
  var q = document.getElementById("query").value;

  var apiKey = "AIzaSyAGw2Lgj16eu4IpoyY1U47zbiashZRy58c";
  var requestURL = `https://www.googleapis.com/youtube/v3/search?part=snippet,id&type=video&q="+
  ${q} + &key=${apiKey} + pageToken=${token}`;

  fetch(requestURL)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log(data); // Console log for debugging
      var nextPageToken = data.nextPageToken;
      var prevPageToken = data.prevPageToken;

      // Dynamically create list items for each video and append to results element
      data.items.forEach((item) => {
        var output = getOutput(item); // getOutput is a function that returns HTML string
        var li = document.createElement("li");
        li.innerHTML = output;
        resultsElement.appendChild(li);
      });

      var buttons = getButtons(prevPageToken, nextPageToken); // returns HTML string for buttons
      buttonsElement.innerHTML = buttons;
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
    });
}
