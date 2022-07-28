window.Telegram.WebApp.ready();
window.Telegram.WebApp.MainButton.setText('Click').show().onClick(() => {
  fetch(
    `https://kittensanswers.ru/menu/?${window.Telegram.WebApp.initData}`,
    {
      method: 'POST',
      headers: { Accept: 'application/json', 'Content-Type': 'application/json' },
    },
  ).then((response) => {
    if (response.ok) {
      window.Telegram.WebApp.close();
    }
  });
});

function createQA(qa, index, qas) {
  const result = document.getElementById('result');
  const qaDiv = document.createElement('div');
  const header = document.createElement('h1');
  header.innerText = qa.title;
  qaDiv.appendChild(header);
  const type = document.createElement('p');
  type.innerText = qa.type;
  qaDiv.appendChild(type);
  qa.answers.forEach((answer) => {
    const answerP = document.createElement('p');
    answerP.innerText = answer;
    qaDiv.appendChild(answerP);
  });
  if (index + 1 !== qas.length) {
    qaDiv.appendChild(document.createElement('hr'));
  }
  result.appendChild(qaDiv);
}

function search(event) {
  const result = document.getElementById('result');
  result.innerHTML = '';
  event.preventDefault();
  axios.get('/menu/json/').then((resp) => {
    resp.data.forEach(createQA);
  });
}

document.getElementById('search').addEventListener('click', search);
