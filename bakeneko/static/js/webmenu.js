window.Telegram.WebApp.ready();

function createQA(qa, index, qas) {
  const result = document.getElementById('result');
  const qaDiv = document.createElement('div');
  const header = document.createElement('h1');
  header.innerText = qa.title;
  qaDiv.appendChild(header);
  const button = document.createElement('button');
  button.setAttribute('id', qa.id);
  button.innerText = 'Send';
  qaDiv.appendChild(button);
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

const result = document.getElementById('result');
result.addEventListener('click', (event) => {
  if (event.target.nodeName !== 'BUTTON') {
    return;
  }
  fetch(
    `/menu/?${window.Telegram.WebApp.initData}`,
    {
      method: 'POST',
      headers: { Accept: 'application/json', 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: event.target.id }),
    },
  ).then((response) => {
    if (response.ok) {
      window.Telegram.WebApp.close();
    }
  });
});

function search(event) {
  result.innerHTML = '';
  event.preventDefault();
  axios.get('/menu/json/').then((resp) => {
    resp.data.forEach(createQA);
  });
}

document.getElementById('search').addEventListener('click', search);
