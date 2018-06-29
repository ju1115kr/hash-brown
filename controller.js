function logIn(iid, ipass) {
var API = 'http://35.234.3.182:9009/api/v1.0/users';

var id = iid;
var password = ipass;

  $.ajax({
    type:'GET',
    dataType: 'json',
    url:'',
    username: iid,
    password: ipass,
    success: funtion(data) {

    }
  });
}

function goToNotice() {
  location.href = "notice.html";
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
  location.href = "";
}
