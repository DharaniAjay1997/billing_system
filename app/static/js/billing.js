// ======================================================
// Billing System - billing.js
// ======================================================

// -------------------------
// DOM Elements
// -------------------------

const billingForm = document.getElementById("billingForm");
const productContainer = document.getElementById("productContainer");
const addProductButton = document.getElementById("addProductBtn");
const resultContainer = document.getElementById("result");

// -------------------------
// Product Row
// -------------------------

function addProductRow() {

    const row = document.createElement("div");

    row.className = "product-row";

    row.innerHTML = `
        <input
            type="text"
            class="product-id"
            placeholder="Product ID"
            required
        />

        <input
            type="number"
            class="quantity"
            placeholder="Quantity"
            min="1"
            value="1"
            required
        />

        <button
            type="button"
            class="remove-product"
        >
            Remove
        </button>

        <br><br>
    `;

    productContainer.appendChild(row);

}

// -------------------------
// Remove Product
// -------------------------

function removeProductRow(event) {

    if (!event.target.classList.contains("remove-product")) {
        return;
    }

    const rows = document.querySelectorAll(".product-row");

    if (rows.length === 1) {
        alert("At least one product is required.");
        return;
    }

    event.target.parentElement.remove();

}

// -------------------------
// Collect Products
// -------------------------

function getProducts() {

    const rows = document.querySelectorAll(".product-row");

    const products = [];

    rows.forEach((row) => {

        products.push({

            product_id: row.querySelector(".product-id").value.trim(),

            quantity: Number(
                row.querySelector(".quantity").value
            )

        });

    });

    return products;

}

// -------------------------
// Collect Denominations
// -------------------------

function getDenominations() {

    const denominations = [];

    document
        .querySelectorAll(".denomination")
        .forEach((input) => {

            denominations.push({

                denomination: Number(
                    input.dataset.value
                ),

                count: Number(
                    input.value
                )

            });

        });

    return denominations;

}

// -------------------------
// Build Request Payload
// -------------------------

function buildRequest() {

    return {

        email: document
            .getElementById("email")
            .value
            .trim(),

        items: getProducts(),

        denominations: getDenominations(),

        cash_paid: Number(
            document.getElementById("cashPaid").value
        )

    };

}

// -------------------------
// Render Invoice
// -------------------------

function renderInvoice(data) {

    let html = `
        <hr>

        <h2>Invoice</h2>

        <p><strong>Invoice:</strong> ${data.invoice_number}</p>

        <p><strong>Email:</strong> ${data.customer_email}</p>

        <p><strong>Subtotal:</strong> ₹${data.subtotal}</p>

        <p><strong>Tax:</strong> ₹${data.tax_amount}</p>

        <p><strong>Grand Total:</strong> ₹${data.grand_total}</p>

        <p><strong>Paid:</strong> ₹${data.cash_paid}</p>

        <p><strong>Balance:</strong> ₹${data.balance_amount}</p>

        <hr>

        <h3>Purchased Products</h3>

        <table border="1" cellpadding="5">

            <tr>
                <th>Product</th>
                <th>Qty</th>
                <th>Price</th>
                <th>Tax</th>
                <th>Total</th>
            </tr>
    `;

    data.items.forEach((item) => {

        html += `
            <tr>

                <td>${item.product_name}</td>

                <td>${item.quantity}</td>

                <td>${item.unit_price}</td>

                <td>${item.tax_amount}</td>

                <td>${item.line_total}</td>

            </tr>
        `;

    });

    html += `
        </table>

        <hr>

        <h3>Return Change</h3>

        <table border="1" cellpadding="5">

            <tr>

                <th>Denomination</th>

                <th>Count</th>

            </tr>
    `;

    data.change.forEach((item) => {

        html += `
            <tr>

                <td>${item.denomination}</td>

                <td>${item.count}</td>

            </tr>
        `;

    });

    html += "</table>";

    resultContainer.innerHTML = html;

}

// -------------------------
// Submit Bill
// -------------------------

async function submitBill(event) {

    event.preventDefault();

    const payload = buildRequest();

    console.log(payload);

    try {

        const response = await fetch(
            "/api/v1/billing",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(payload)

            }
        );

        const data = await response.json();

        if (!response.ok) {

            alert(data.detail || "Unable to generate bill.");

            return;

        }

        renderInvoice(data);

        alert("Bill generated successfully.");

    }

    catch (error) {

        console.error(error);

        alert("Server Error.");

    }

}

// -------------------------
// Register Events
// -------------------------

function registerEvents() {

    addProductButton.addEventListener(
        "click",
        addProductRow
    );

    productContainer.addEventListener(
        "click",
        removeProductRow
    );

    billingForm.addEventListener(
        "submit",
        submitBill
    );

}

// -------------------------
// Initialize
// -------------------------

function init() {

    addProductRow();

    registerEvents();

}

document.addEventListener(
    "DOMContentLoaded",
    init
);