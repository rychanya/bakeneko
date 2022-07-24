Telegram.WebApp.ready();
Telegram.WebApp.MainButton.setText('Click').show().onClick(function () {
    console.log(Telegram.WebApp.initDataUnsafe);
    console.log(Telegram.WebApp.initData);
    fetch("https://kittensanswers.ru/menu/?" + Telegram.WebApp.initData,
        {
            method: 'POST',
            headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' }
        }
    ).then(function (response) {
        if (response.ok) {
            Telegram.WebApp.close()
        }
    })
})