// 搜索框監聽
document.getElementById("search-form").addEventListener("submit", function (e) {
  e.preventDefault();
  const q = document.getElementById("query").value;
  loadVideos("", q);
});

// 上/下頁按鈕監聽
document.getElementById("buttons").addEventListener("click", function (e) {
  if (e.target.classList.contains("paging-button")) {
    e.preventDefault();
    const token = e.target.getAttribute("data-token");
    const q = e.target.getAttribute("data-query");
    loadVideos(token, q);
  }
});

// Load search lists
function loadVideos(token = "") {
  const q = document.getElementById("query").value;
  const apiKey = "AIzaSyA_PGKxKojyjZLjb_tNUV9pLq6DgwtGcSI"; // 因為目前demo是丟到github page，目前沒查詢到保護的機制
  const requestURL =
    `https://www.googleapis.com/youtube/v3/search?part=snippet,id&type=video&q=${q}&key=${apiKey}` +
    (token ? `&pageToken=${token}` : "");

  fetch(requestURL)
    .then((response) => {
      if (!response.ok) throw new Error("Network response was not ok");
      return response.json();
    })
    .then((data) => {
      const resultsElement = document.getElementById("results");
      const buttonsElement = document.getElementById("buttons");
      resultsElement.innerHTML = ""; // Clear previous results
      buttonsElement.innerHTML = ""; // Clear previous results

      data.items.forEach(
        (item) => (resultsElement.innerHTML += getOutput(item))
      );
      buttonsElement.innerHTML = getButtons(
        data.prevPageToken,
        data.nextPageToken,
        q
      ); // 將q傳遞到下一個page
    })
    .catch((error) =>
      console.error("There was a problem with the fetch operation:", error)
    );
}

// Build html Output
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
function getButtons(prevPageToken, nextPageToken, query) {
  let buttonsHtml = '<div class="button-container">';

  if (prevPageToken) {
    buttonsHtml += `<button id="prev-button" class="paging-button" data-token="${prevPageToken}" data-query="${query}">Prev Page</button>`;
  }

  if (nextPageToken) {
    buttonsHtml += `<button id="next-button" class="paging-button" data-token="${nextPageToken}" data-query="${query}">Next Page</button>`;
  }

  buttonsHtml += "</div>";
  return buttonsHtml;
}
