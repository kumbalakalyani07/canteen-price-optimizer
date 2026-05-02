import tkinter as tk
from tkinter import ttk, messagebox

def safe_float(x, name):
    try:
        v = float(x)
        return v
    except:
        raise ValueError(f"Enter a valid number for {name}")

def compute():
    try:
        product = product_var.get().strip() or "Item"

        p1 = safe_float(p1_var.get(), "Price 1")
        q1 = safe_float(q1_var.get(), "Demand at Price 1")
        p2 = safe_float(p2_var.get(), "Price 2")
        q2 = safe_float(q2_var.get(), "Demand at Price 2")
        cost = safe_float(cost_var.get(), "Cost per unit")

        if p1 <= 0 or p2 <= 0:
            raise ValueError("Prices must be > 0")
        if q1 < 0 or q2 < 0:
            raise ValueError("Demands must be >= 0")
        if p1 == p2:
            raise ValueError("Price 1 and Price 2 must be different")
        if cost < 0:
            raise ValueError("Cost must be >= 0")

        # Linear demand: Q = a - bP
        b = (q1 - q2) / (p2 - p1)
        a = q1 + b * p1

        if b <= 0:
            raise ValueError(
                "Your inputs do not form a downward-sloping demand curve.\n"
                "Try: higher price should have lower demand."
            )

        # clear old rows
        for item in tree.get_children():
            tree.delete(item)

        # Search price range
        min_price = max(0.5, min(p1, p2) * 0.5)
        max_price = max(p1, p2) * 1.8

        step = safe_float(step_var.get(), "Step (₹)")
        if step <= 0:
            raise ValueError("Step must be > 0")

        best = None
        price = min_price

        while price <= max_price + 1e-9:
            demand = a - b * price
            if demand < 0:
                demand = 0

            revenue = price * demand
            profit = (price - cost) * demand

            if best is None or profit > best["profit"]:
                best = {
                    "price": price,
                    "demand": demand,
                    "revenue": revenue,
                    "profit": profit
                }

            tree.insert(
                "", "end",
                values=(
                    f"{price:.2f}",
                    f"{demand:.1f}",
                    f"{revenue:.2f}",
                    f"{profit:.2f}"
                )
            )
            price += step

        # Output summary
        demand_eq_label.config(text=f"Demand Equation: Q = {a:.2f} - {b:.2f}P")
        summary_label.config(
            text=(
                f"Best Price for {product}: ₹{best['price']:.2f}\n"
                f"Expected Demand: {best['demand']:.1f} units/day\n"
                f"Revenue: ₹{best['revenue']:.2f} per day\n"
                f"Profit: ₹{best['profit']:.2f} per day"
            )
        )

        # Simple insight message (for viva/assignment)
        if best["price"] < cost:
            insight = "⚠️ Best price came below cost (loss). Increase demand or reduce cost."
        elif best["demand"] == 0:
            insight = "⚠️ Demand becomes zero in your tested range. Try different input points."
        else:
            insight = "✅ This price balances demand drop vs margin increase to maximize profit."
        insight_label.config(text=insight)

    except Exception as e:
        messagebox.showerror("Input Error", str(e))

# ---------------- UI ----------------
root = tk.Tk()
root.title("Campus Canteen Price Optimizer (Demand–Supply)")
root.geometry("900x600")

top = tk.Frame(root)
top.pack(fill="x", padx=12, pady=10)

tk.Label(top, text="Campus Canteen Price Optimizer", font=("Arial", 18, "bold")).pack(anchor="w")
tk.Label(top, text="Enter 2 price–demand points to estimate a demand curve. App finds the price that maximizes profit.",
         font=("Arial", 10)).pack(anchor="w", pady=2)

form = tk.LabelFrame(root, text="Inputs", padx=10, pady=10)
form.pack(fill="x", padx=12, pady=8)

product_var = tk.StringVar(value="Momos")

p1_var = tk.StringVar(value="30")
q1_var = tk.StringVar(value="120")
p2_var = tk.StringVar(value="50")
q2_var = tk.StringVar(value="70")

cost_var = tk.StringVar(value="18")
step_var = tk.StringVar(value="1")

row1 = tk.Frame(form); row1.pack(fill="x", pady=4)
tk.Label(row1, text="Product name:", width=18, anchor="w").pack(side="left")
tk.Entry(row1, textvariable=product_var, width=20).pack(side="left", padx=6)

row2 = tk.Frame(form); row2.pack(fill="x", pady=4)
tk.Label(row2, text="Price 1 (₹):", width=18, anchor="w").pack(side="left")
tk.Entry(row2, textvariable=p1_var, width=10).pack(side="left", padx=6)
tk.Label(row2, text="Demand at Price 1 (units/day):", width=26, anchor="w").pack(side="left")
tk.Entry(row2, textvariable=q1_var, width=10).pack(side="left", padx=6)

row3 = tk.Frame(form); row3.pack(fill="x", pady=4)
tk.Label(row3, text="Price 2 (₹):", width=18, anchor="w").pack(side="left")
tk.Entry(row3, textvariable=p2_var, width=10).pack(side="left", padx=6)
tk.Label(row3, text="Demand at Price 2 (units/day):", width=26, anchor="w").pack(side="left")
tk.Entry(row3, textvariable=q2_var, width=10).pack(side="left", padx=6)

row4 = tk.Frame(form); row4.pack(fill="x", pady=4)
tk.Label(row4, text="Cost per unit (₹):", width=18, anchor="w").pack(side="left")
tk.Entry(row4, textvariable=cost_var, width=10).pack(side="left", padx=6)
tk.Label(row4, text="Price step (₹):", width=26, anchor="w").pack(side="left")
tk.Entry(row4, textvariable=step_var, width=10).pack(side="left", padx=6)

btn_row = tk.Frame(form); btn_row.pack(fill="x", pady=8)
tk.Button(btn_row, text="Calculate Best Price", command=compute, height=1).pack(side="left")

demand_eq_label = tk.Label(root, text="Demand Equation: —", font=("Arial", 11, "bold"))
demand_eq_label.pack(anchor="w", padx=12, pady=(6, 0))

summary_label = tk.Label(root, text="Best Price Summary will appear here.", font=("Arial", 12))
summary_label.pack(anchor="w", padx=12, pady=6)

insight_label = tk.Label(root, text="", font=("Arial", 10))
insight_label.pack(anchor="w", padx=12, pady=(0, 6))

table_frame = tk.LabelFrame(root, text="Price vs Demand vs Revenue vs Profit (Table)", padx=8, pady=8)
table_frame.pack(fill="both", expand=True, padx=12, pady=10)

cols = ("Price (₹)", "Demand (units/day)", "Revenue (₹/day)", "Profit (₹/day)")
tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)
for c in cols:
    tree.heading(c, text=c)
    tree.column(c, anchor="center", width=170)

scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scroll.set)

tree.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

footer = tk.Label(root, text="Tip: Use realistic points: higher price → lower demand.", font=("Arial", 9))
footer.pack(anchor="w", padx=12, pady=(0, 10))

root.mainloop()
