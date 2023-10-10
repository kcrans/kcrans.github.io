document.getElementById('CopyButton').addEventListener('click', function(event) {
  event.stopPropagation();  // Prevent triggering the default <summary> behavior
  var textToCopy = document.getElementById('pgp_key').textContent;
  var clippy = document.getElementById('clipboard_svg');
  var checky = document.getElementById('checkmark_svg');
  var texty = document.getElementById('button_text');
  
  navigator.clipboard.writeText(textToCopy).then(() => {
    clippy.style.display = 'none';
    checky.style.display = 'block';
    texty.textContent = "Copied!";
  }).catch(err => {
    console.error('Unable to copy text: ', err);
  });

  setTimeout(() => {
    clippy.style.display = 'block';
    checky.style.display = 'none';
    texty.textContent = "Copy key";
  }, 3000)
});
