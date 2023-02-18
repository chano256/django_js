const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appOutput = document.querySelector(".app-output");
const paginationContainer = document.querySelector(".pagination-container");

tableOutput.style.display = "none";

searchField.addEventListener('keyup', (e) => {
    const searchValue = e.target.value;

    if (searchValue.trim().length > 3) {
        tableOutput.style.display = "none";
        appOutput.style.display = "none";

         fetch('/search-expenses', {
            body: JSON.stringify({ searchText: searchValue }),
            method: "POST",
         }).then((res) => res.json())
             .then((data) => {
                appOutput.style.display = "none";
                tableOutput.style.display = "block";

                if (data.length === 0) {
                    tableOutput.innerHTML = 'No Results Found';
                }
        });
    } else {
        tableOutput.style.display = 'none'
        appOutput.style.display = "block";
        paginationContainer.style.display = "block";
    }
});