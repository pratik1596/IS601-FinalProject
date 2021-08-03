let alertbutton = document.querySelector('.alert button');

if (alertbutton){
  alertbutton.addEventListener('click', function (event) {

  	if (!event.target === alertbutton) return;
    alertbutton.parentNode.style.display = 'none';

  	event.preventDefault();

  }, false);
}