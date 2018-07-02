function logIn(iid, ipass) {
  var id = iid
  var password = ipass
  if (id === "") {
    alert("아이디를 입력해 주세요.")
  } else if (id !== "" && password === "") {
    alert("패스워드를 입력 해 주세요.")
  } else {
    $.ajax({
      type: 'GET',
      url: "http://35.234.3.182:9009/api/v1.0/users",
      beforeSend: function(xhr) {
        xhr.setRequestHeader("Authorization", "Basic " + btoa(id + ":" + password));
      },
      data: {},
      success: function(data) {
        alert("로그인 되었습니다.");
        $("#id").remove();
        $("#password").remove();
        $("#loginButton").remove();
        $("#log").append("<img src = '../resources/hyogyung.jpg' style = 'width: 50px, height: auto'></img>");
      },
      error: function() {
        alert("아이디 또는 패스워드가 틀렸습니다");
      }
    })
  }
}

function goToNotice() {
  location.href = "notice.html";
  $("#notice").css("text-color", "red");
}

function goToPopular() {
  location.href = "popular.html";
}

function goToDashboard() {
  location.href = "dashboard.html";
}

function goToRanking() {
  location.href = "";
}

function goToWritePage() {
  location.href = "posting.html";
}
