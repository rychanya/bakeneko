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
