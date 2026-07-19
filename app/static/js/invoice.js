const invoiceContainer = document.getElementById(
    "invoiceContainer"
);

async function loadInvoice() {

    try {

        const response = await fetch(
            `/api/v1/billing/${billId}`
        );

        if (!response.ok) {

            alert("Unable to load invoice.");

            return;

        }

        const bill = await response.json();

        renderInvoice(bill);

    }

    catch (error) {

        console.error(error);

        alert("Server Error");

    }

}

function renderInvoice(bill) {

    let html = `
    
        <h2>${bill.invoice_number}</h2>

        <p>

            <strong>Email :</strong>

            ${bill.customer.email}

        </p>

        <p>

            <strong>Date :</strong>

            ${new Date(
                bill.created_at
            ).toLocaleString()}

        </p>

        <table border="1" width="100%">

            <thead>

                <tr>

                    <th>Product</th>

                    <th>Qty</th>

                    <th>Price</th>

                    <th>Tax %</th>

                    <th>Tax</th>

                    <th>Total</th>

                </tr>

            </thead>

            <tbody>

    `;

    bill.items.forEach(item => {

        html += `

            <tr>

                <td>${item.product.name}</td>

                <td>${item.quantity}</td>

                <td>${item.unit_price}</td>

                <td>${item.tax_percentage}%</td>

                <td>${item.tax_amount}</td>

                <td>${item.line_total}</td>

            </tr>

        `;

    });

    html += `

        </tbody>

        </table>

        <br>

        <h3>Summary</h3>

        <p>Subtotal : ₹${bill.subtotal}</p>

        <p>Tax : ₹${bill.tax_amount}</p>

        <p>Grand Total : ₹${bill.grand_total}</p>

        <p>Cash Paid : ₹${bill.cash_paid}</p>

        <p>Balance : ₹${bill.balance_amount}</p>

    `;

    invoiceContainer.innerHTML = html;

}

loadInvoice();