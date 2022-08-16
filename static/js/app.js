window.addEventListener('load', () => {
  const toggleBtn = document.getElementById('toggle-btn');
  const list = document.querySelector('#list');
  const closeBtn = document.querySelector('.close-btn');
  const sidebar = document.querySelector('.sidebar-wrapper');
  const info = document.querySelector('.info');
  toggleBtn.addEventListener('click', () => {
    list.classList.toggle('show-lists');
  });

  closeBtn.addEventListener('click', () => {
    sidebar.classList.remove('show');
  });

  info.addEventListener('click', () => {
    sidebar.classList.add('show');
  });
  const returnBtn = document.getElementById('return-btn');
  const returnHover = document.querySelector('.return-hover');
  console.log(returnBtn);
  console.log(returnHover);
  returnBtn.addEventListener('click', () => {
    returnHover.classList.add('show-hover');
  });
  returnBtn.addEventListener('mouseout', () => {
    returnHover.classList.remove('show-hover');
  });
  // console.log('Working');
});
