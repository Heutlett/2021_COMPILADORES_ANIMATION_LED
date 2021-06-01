import tkinter as tk
root = tk.Tk()


file1data = ("qUdYzh5H5ilpZZQ6gFklTt3JFy8rTy2QSGQip0blDWj18VIkxBEAHTL1\n8xf1S1tGbmvb0laqYx1gTsrDa3nnkTR6KstOWvJiWpY4v308Mtw5NIEq8sYRt0mFoR0WzHVvak7RmOHR0v3VijwfPRGBq93nIsTxGJVuvWYnPGUDXciuS650s6pbdOtzKaSKaWf2jFFAIBEgwpWNTrQSLkKgg0h5eA8IYdnrrroXsak3Oiq3asU7tThnUPps1rRl2oXe8e0ZxkWL34kjB1cX3lGae7ixys7nRUQJYiFWUeVsE19u31gPxxy5mzrf9bgkP055Dk5Oquwyeg0tWBsIeMatJd1cgm5cbsgXwM0wuBjeKTFg6MCWQCSFrUpVlr0Uz3ZNEOCDKVe\nPhGDSOJnNbe6Qvx41GeDIRBXdVw12PrD8QWAGK2OPQ5FfwgObBmMV3cEYlQJGNgXowTICaUfNQRfpuGN5CnoksIQ4E4MaOv13dnIpUPXWc3QCu1bf3cmhNoUPrXcxVi7ZkJ\n8AtvtRrdZSNUU34msnNrFIPNBoJmqkZTr7E3QCMHyMfZbVQwaThO5q1OCfOA2oZ26VZHzZamTXGleH\nVXoARH0OQ0XFZsYwwz8tnWqtPuAzAVcjJtdUNxrPbKFlPei1MzschurpyvTwe9pi86oKp1P72XDUhnvJ3kAfRj1kjxSeQFEGX28Op0PtOzoc2taGlgyLO5THiLruSnLNBVKZMt9wBefu4vtjB8riD7itodprVoT960YlDGgQdY93hAPuyb8O6qn3olYbrm0Hp65XpSRZoWjo09")

def viewall(*args):
    template1.yview(*args)
    template2.yview(*args)

xscrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
xscrollbar.grid(row=4, column=6, columnspan=4)
xscrollbar.config(command=viewall)

template1 = tk.Text(root, height=50, width=50,yscrollcommand = xscrollbar.set)
template1.grid(row=5, column=0)
template1.insert(tk.END, file1data)

template2 = tk.Text(root, height=50, width=50, yscrollcommand = xscrollbar.set)
template2.grid(row=5, column=1)
template2.insert(tk.END, file1data)

tk.mainloop()