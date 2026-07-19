const searchBtn = document.getElementById("searchBtn");
const historyBody = document.getElementById("historyBody");
const emailInput = document.getElementById("email");

async function searchHistory() {

    const email = emailInput.value.trim();

    if (!email) {

        alert("Enter customer email.");

        return;
    }

    const response = await fetch(
        `/api/v1/billing/history/${encodeURIComponent(email)}`
    );

    const bills = await response.json();

    historyBody.innerHTML = "";

    bills.forEach(bill => {

        historyBody.innerHTML += `
            <tr>

                <td>${bill.invoice_number}</td>

                <td>${new Date(
                    bill.created_at
                ).toLocaleString()}</td>

                <td>₹${bill.grand_total}</td>

                <td>

                    <button
                        onclick="viewInvoice(${bill.id})"
                    >
                        View
                    </button>

                </td>

            </tr>
        `;

    });

}

function viewInvoice(id){

    window.location.href =
        `/invoice/${id}`;

}

searchBtn.addEventListener(
    "click",
    searchHistory
);