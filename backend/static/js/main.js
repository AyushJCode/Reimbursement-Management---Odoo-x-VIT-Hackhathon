/** * ODOO REIMBURSEMENT SYSTEM - FINAL HACKATHON BUILD
 * Features: Multi-tenant Login, Currency Conversion, Real-time Approval Queue
 */

// --- 1. AUTHENTICATION ---
async function login() {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    if (!email || !password) {
        alert("Please enter both email and password.");
        return;
    }

    try {
        const res = await fetch('/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (res.ok) {
            // Transition from Login to Dashboard [cite: 50]
            document.getElementById('loginSection').classList.add('hidden');
            document.getElementById('dashboard').classList.remove('hidden');
            document.getElementById('welcomeMsg').innerText = `Odoo | ${data.role} Dashboard`;

            // Role-Based UI: Only Admins/Managers see the Approval Queue [cite: 88, 89]
            if (data.role === 'Admin' || data.role === 'Manager') {
                document.getElementById('managerSection').classList.remove('hidden');
                loadPending();
            }
            loadHistory();
        } else {
            alert(data.error || "Invalid Credentials");
        }
    } catch (err) {
        console.error("Login Error:", err);
    }
}

// --- 2. LOAD EMPLOYEE HISTORY ---
async function loadHistory() {
    const res = await fetch('/expenses/my-history');
    const data = await res.json();
    const tbody = document.querySelector('#histTable tbody');
    const thead = document.querySelector('#histTable thead');
    
    // Reset view to History [cite: 61, 91]
    document.getElementById('welcomeMsg').innerText = "My Expenses";
    thead.innerHTML = '<tr><th>Date</th><th>Category</th><th>Amount</th><th>Status</th></tr>';
    
    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted">No expenses submitted yet.</td></tr>';
        return;
    }

    tbody.innerHTML = data.map(ex => `
        <tr>
            <td>${ex.date}</td>
            <td class="fw-bold">${ex.category}</td>
            <td>${ex.currency} ${ex.amount}</td>
            <td><span class="status-${ex.status.toLowerCase()}">${ex.status}</span></td>
        </tr>
    `).join('');
}

// --- 3. LOAD ANALYTICS REPORTS ---
async function showReports() {
    const res = await fetch('/expenses/stats');
    const data = await res.json();
    const tbody = document.querySelector('#histTable tbody');
    const thead = document.querySelector('#histTable thead');
    
    document.getElementById('welcomeMsg').innerText = "Expense Analytics";
    thead.innerHTML = '<tr><th>Category</th><th>Total Approved (INR)</th></tr>';
    
    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="2" class="text-center">No approved data available.</td></tr>';
    } else {
        tbody.innerHTML = data.map(stat => `
            <tr>
                <td><span class="badge bg-secondary">${stat.category}</span></td>
                <td><strong>₹${stat.total.toLocaleString()}</strong></td>
            </tr>
        `).join('');
    }
}

// --- 4. LOAD MANAGER APPROVAL QUEUE ---
async function loadPending() {
    const res = await fetch('/approvals/pending');
    const data = await res.json();
    const container = document.getElementById('pendTable');
    
    if (data.length === 0) {
        container.innerHTML = '<p class="text-muted text-center py-4">No pending claims ✅</p>';
        return;
    }

    // Amount is shown in Company Default Currency (INR) [cite: 90]
    container.innerHTML = data.map(ex => `
        <div class="card mb-3 p-3 border-0 shadow-sm border-start border-4 border-primary">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <h6 class="mb-0 fw-bold">${ex.category}</h6>
                    <small class="text-muted">${ex.date} | User #${ex.user_id}</small>
                </div>
                <span class="text-success fw-bold">₹${ex.converted_amount}</span>
            </div>
            <div class="d-flex gap-2 mt-3">
                <button onclick="handleAction(${ex.id}, 'approve')" class="btn btn-sm btn-success flex-grow-1">Approve</button>
                <button onclick="handleAction(${ex.id}, 'reject')" class="btn btn-sm btn-outline-danger flex-grow-1">Reject</button>
            </div>
        </div>
    `).join('');
}

// --- 5. APPROVE/REJECT ACTIONS ---
async function handleAction(id, action) {
    const res = await fetch('/approvals/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ expense_id: id, action: action })
    });

    if (res.ok) {
        loadPending(); // Refresh Manager Queue [cite: 73, 75]
        loadHistory(); // Refresh Personal History
    }
}

// --- 6. EXPENSE SUBMISSION ---
document.getElementById('expForm').onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    const res = await fetch('/expenses/add-expense', {
        method: 'POST',
        body: formData
    });

    if (res.ok) {
        // Close Modal [cite: 59, 60]
        const modalEl = document.getElementById('expenseModal');
        const modal = bootstrap.Modal.getInstance(modalEl);
        modal.hide();
        
        e.target.reset();
        
        // Immediate UI Sync: Refresh both lists so the claim appears instantly
        loadHistory();
        loadPending(); 
        
        console.log("Expense submitted and UI synchronized.");
    } else {
        alert("Submission failed. Check your data.");
    }
};