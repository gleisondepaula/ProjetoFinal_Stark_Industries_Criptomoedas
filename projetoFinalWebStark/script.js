document.addEventListener("DOMContentLoaded", function() {
    const cryptoListSection = document.getElementById("crypto-list");
    const filterInput = document.getElementById("filter-input");
    const filterBtn = document.getElementById("filter-btn");
    const currencySelect = document.getElementById("currency");
    const amountInput = document.getElementById("amount");
    const convertBtn = document.getElementById("convert-btn");
    const conversionResult = document.getElementById("conversion-result");

    // Função para buscar informações das criptomoedas e moedas disponíveis
    function getCryptoData() {
        const apiUrl = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false";

        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                // Limpa a lista de criptomoedas
                cryptoListSection.innerHTML = "";

                // Popula o seletor de moedas
                currencySelect.innerHTML = "";
                data.forEach(crypto => {
                    const option = document.createElement("option");
                    option.value = crypto.symbol;
                    option.textContent = crypto.symbol.toUpperCase();
                    currencySelect.appendChild(option);
                });

                // Itera sobre os dados e cria um card para cada criptomoeda
                data.forEach(crypto => {
                    const card = document.createElement("div");
                    card.classList.add("crypto-card");
                    card.innerHTML = `
                        <img src="${crypto.image}" alt="${crypto.name}" class="crypto-logo">
                        <h3>${crypto.name}</h3>
                        <p>Cotação: ${crypto.current_price} USD</p>
                        <p>Data: ${new Date().toLocaleDateString()}</p>
                        <p>Descrição: ${crypto.description || 'Descrição não disponível'}</p>
                    `;
                    cryptoListSection.appendChild(card);
                });
            })
            .catch(error => console.error("Erro ao buscar dados das criptomoedas:", error));
    }

    // Função para filtrar as criptomoedas pelo nome
    function filterCrypto() {
        const filterValue = filterInput.value.toLowerCase();
        const cryptoCards = document.querySelectorAll(".crypto-card");

        cryptoCards.forEach(card => {
            const cryptoName = card.querySelector("h3").textContent.toLowerCase();
            if (cryptoName.includes(filterValue)) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    }

    // Função para realizar a conversão de moedas
    function convertCurrency() {
        const selectedCurrency = currencySelect.value;
        const amount = parseFloat(amountInput.value);

        if (isNaN(amount)) {
            conversionResult.textContent = "Insira um valor válido para a quantidade.";
            return;
        }

        const apiUrl = `https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=${selectedCurrency}`;

        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                const exchangeRate = data.bitcoin[selectedCurrency];
                if (exchangeRate) {
                    const convertedAmount = amount * exchangeRate;
                    conversionResult.textContent = `${amount} USD = ${convertedAmount} ${selectedCurrency}`;
                } else {
                    conversionResult.textContent = "Moeda selecionada não suportada.";
                }
            })
            .catch(error => console.error("Erro ao converter moeda:", error));
    }

    // Event listeners para acionar as funções
    filterBtn.addEventListener("click", filterCrypto);
    convertBtn.addEventListener("click", convertCurrency);

    // Chamada inicial para buscar as informações das criptomoedas
    getCryptoData();
});
