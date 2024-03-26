// 確保DOM完全加載並解析後，才執行loadCurrencies函數
// 也確保在向<select>元素中動態添加國家代碼選項時，相關的DOM元素已經可用
document.addEventListener("DOMContentLoaded", function () {
  loadCurrencies();
  document.getElementById("currency-one").addEventListener("change", calculate);
  document.getElementById("amount-one").addEventListener("input", calculate);
  document.getElementById("currency-two").addEventListener("change", calculate);
  document.getElementById("amount-two").addEventListener("input", calculate);
  document.getElementById("swap").addEventListener("click", swapCurrencies);
  calculate();
});

// Load the Supported CODE
function loadCurrencies() {
  fetch(
    "https://v6.exchangerate-api.com/v6/61cbd2fff64362a25710100e/latest/USD"
  )
    .then((response) => response.json())
    .then((data) => {
      const currencyOneSelect = document.getElementById("currency-one");
      const currencyTwoSelect = document.getElementById("currency-two");

      // loop inserting CODE
      Object.keys(data.conversion_rates).forEach((key) => {
        const optionOne = new Option(key, key);
        const optionTwo = new Option(key, key);
        currencyOneSelect.add(optionOne);
        currencyTwoSelect.add(optionTwo);
      });

      // default
      currencyOneSelect.value = "USD";
      currencyTwoSelect.value = "TWD";

      calculate();
    })
    .catch((error) => console.error("Error loading currencies:", error));
}

// Calculate exchange currency
function calculate() {
  const currencyOne = document.getElementById("currency-one").value;
  const currencyTwo = document.getElementById("currency-two").value;
  const amountOne = document.getElementById("amount-one").value;

  fetch(
    `https://v6.exchangerate-api.com/v6/61cbd2fff64362a25710100e/latest/${currencyOne}`
  )
    .then((res) => res.json())
    .then((data) => {
      const rate = data.conversion_rates[currencyTwo];
      document.getElementById(
        "rate"
      ).innerText = `1 ${currencyOne} = ${rate} ${currencyTwo}`;
      document.getElementById("amount-two").value = (amountOne * rate).toFixed(
        2
      );
    });
}

// Swap
function swapCurrencies() {
  const currencyOneSelect = document.getElementById("currency-one");
  const currencyTwoSelect = document.getElementById("currency-two");

  const temp = currencyOneSelect.value;
  currencyOneSelect.value = currencyTwoSelect.value;
  currencyTwoSelect.value = temp;

  calculate();
}
