(function(){
  var speakWord = "Hello";
  window.helloSpeaker = {};
  helloSpeaker.speak = function(name) {
    console.log(speakWord + " " + name);
  }
})();
