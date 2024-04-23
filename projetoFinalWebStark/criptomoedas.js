// function getCryptoData(callback) {
//     var url = "https://api.coingecko.com/api/v3/coins/markets";
//     var params = {
//         vs_currency: "usd",
//         order: "market_cap_desc",
//         per_page: 10,
//         page: 1,
//         sparkline: false
//     };

//     $.ajax({
//         url: url,
//         data: params,
//         success: function(data) {
//             callback(data);
//         },
//         error: function(xhr, status, error) {
//             console.error("Erro ao obter dados das criptomoedas:", error);
//         }
//     });
// }
