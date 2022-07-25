Telegram.WebApp.ready();
Telegram.WebApp.MainButton.setText('Click').show().onClick(() => {
  fetch(
    `https://kittensanswers.ru/menu/?${Telegram.WebApp.initData}`,
    {
      method: 'POST',
      headers: { Accept: 'application/json', 'Content-Type': 'application/json' },
    },
  ).then((response) => {
    if (response.ok) {
      Telegram.WebApp.close();
    }
  });
});
