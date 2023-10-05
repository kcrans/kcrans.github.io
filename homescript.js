document.getElementById('CopyButton').addEventListener('click', function(event) {
    event.stopPropagation();  // Prevent triggering the default <summary> behavior
    
    var textToCopy = document.getElementById('pgp_key').textContent;
    var textArea = document.createElement('textarea');
    textArea.value = textToCopy;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);

    alert('Text copied to clipboard!');
});
