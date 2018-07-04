function openAssocNews (e) {
  e = e || window.event;
  var target = e.target || e.srcElement;
  var news_id = target.id;
  var url = "news_view.html?news_id=" + news_id;
  location.href = url;
}

function writeFors () {
  location.href = "temp.html"//글쓰기 url
}

function writeAgainsts () {
  location.href= "temp.html"//글쓰기 url
}

function authorInfo (url) {
  location.href = url;
}

function editNews () {
  jsondata = JSON.stringify({
      field: $("#sub").val(),
      title: $("#titlebox").val(),
      context: $("textarea#postBox").val()
  });
  $.ajax({
    type: 'put',
    url: 'http://35.234.3.182:9009/api/v1.0/news/3',
    contentType: 'application/json; charset=utf-8',
    traditional: true,
    async: false,
    data: jsondata,
    beforeSend: function (xhr) {
      xhr.setRequestHeader("Authorization", "Basic " + btoa('jiyoon075' + ":" + 'rlawldbs'));
    },
    success: function (data) {
      console.log(data);
    },
    error: function (xhr) {
      if (xhr.status == 403) {
        alert("자신의 글이 아닌 것은 수정할 수 없습니다.")
      }
    }
  })
}

function deleteNews () {
  $.ajax({
    type: 'delete',
    url: 'http://35.234.3.182:9009/api/v1.0/news/1',
    contentType: 'application/json; charset=utf-8',
    traditional: true,
    async: false,
    data: {},
    beforeSend: function (xhr) {
      xhr.setRequestHeader("Authorization", "Basic " + btoa('jiyoon075' + ":" + 'rlawldbs'));
    },
    success: function (data) {
      console.log(data);
    },
    error: function (xhr) {
      if (xhr.status == 403) {
        alert("자신의 글이 아닌 것은 삭제할 수 없습니다.")
      }
    }
  })
}

function clickStar () {
  var img = document.getElementById('starimg');
  if (img.src.match("star")) {
    $.ajax({
      type: 'post',
      url: 'http://35.234.3.182:9009/api/v1.0/news/4/star',
      contentType: 'application/json; charset=utf-8',
      traditional: true,
      async: false,
      data: {},
      beforeSend: function (xhr) {
          xhr.setRequestHeader("Authorization", "Basic " + btoa('jiyoon075' + ":" + 'rlawldbs'));
      },
      success: function (data) {
        img.src = "resources/empty.png";
        var startag = document.getElementById('starCount');
        var starvalue = document.createTextNode(data.stars[0]);
        startag.removeChild(startag.childNodes[0]);
        //$('#starCount').remove();
        $('#starCount').append(starvalue);
        console.log(starvalue);
      },
    })
  }
  else {
    img.src = "resources/star.jpg";
    $.ajax({
      type: 'delete',
      url: 'http://35.234.3.182:9009/api/v1.0/news/4/star',
      contentType: 'application/json; charset=utf-8',
      traditional: true,
      async: false,
      data: {},
      beforeSend: function (xhr) {
          xhr.setRequestHeader("Authorization", "Basic " + btoa('jiyoon075' + ":" + 'rlawldbs'));
      },
      success: function (data) {
        console.log(data);
        var startag = document.getElementById('starCount');
        var starvalue = startag.childNodes[0].nodeValue;
        starvalue = parseInt(starvalue) -1;
        startag.removeChild(startag.childNodes[0]);
        $('#starCount').append(starvalue);
      },
    })
  }
}
