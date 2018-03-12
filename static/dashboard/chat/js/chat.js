$(document).ready(function () {

    var config = {
        apiKey: "AIzaSyB804F8eGGoUg_HThtuJT9o80gAapjNV0k",
        authDomain: "test-72ce0.firebaseapp.com",
        databaseURL: "https://test-72ce0.firebaseio.com",
        projectId: "test-72ce0",
        storageBucket: "test-72ce0.appspot.com",
        messagingSenderId: "781009340958"
    };
    firebase.initializeApp(config);

    // firebase.auth().signInAnonymously().catch(function (error) {
    //     var errorCode = error.code;
    //     var errorMessage = error.message;
    //     // ...
    // });

    var starCountRef = firebase.database().ref('categories/').orderByChild('date');
    starCountRef.on('value', function (snapshot) {
        //$("#lista_cats").remove();
        snapshot.forEach(function (item) {
            var itemVal = item.val();
            if ($("#cat" + item.key).length) {
                $("#cat" + item.key).replaceWith("<a href='#' class='list-group-item justify-content-between list-group-item-action' id='" + "cat" + item.key + "'>" + "<img src='" + itemVal.image + "' class='rounded-circle'>" + itemVal.name + "<img src='https://s3.amazonaws.com/linkup-photos/82cffad1-e6f8-4f75-a711-a33c3f272131.png' class=''></a>");
            }
            else {
                $("#lista_cats").append("<a href='#' class='list-group-item justify-content-between list-group-item-action' id='" + "cat" + item.key + "'>" + "<img src='" + itemVal.image + "' class='rounded-circle'>" + itemVal.name + "<img src='https://s3.amazonaws.com/linkup-photos/82cffad1-e6f8-4f75-a711-a33c3f272131.png' class=''></a>");
            }
        });
    });

});