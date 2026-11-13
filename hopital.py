import tkinter as tk
from tkinter import messagebox
import threading
import time

class HopitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hopital Central - Systeme de Guichet Pro")
        self.root.geometry("850x650")
        self.root.config(bg="#0b0f19")

        # Variables
        self.user_name = ""
        self.selected_specialty = ""
        self.selected_doctor = ""
        self.selected_room = ""
        self.my_ticket = 16
        self.current_called = 12
        self.running_queue = False

        # --- FRAME DE CONNEXION ---
        self.login_frame = tk.Frame(root, bg="#111827", padx=30, pady=30)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=450, height=400)

        tk.Label(self.login_frame, text="Hopital Central", font=("Segoe UI", 20, "bold"), bg="#111827", fg="#0284c7").pack(pady=10)
        tk.Label(self.login_frame, text="Connexion Patient", font=("Segoe UI", 12), bg="#111827", fg="#9ca3af").pack(pady=5)

        tk.Label(self.login_frame, text="Nom :", font=("Segoe UI", 10, "bold"), bg="#111827", fg="#d1d5db", anchor="w").pack(fill="x", pady=2)
        self.nom_entry = tk.Entry(self.login_frame, font=("Segoe UI", 11), bg="#1f2937", fg="white", insertbackground="white")
        self.nom_entry.pack(fill="x", pady=5)

        tk.Label(self.login_frame, text="Prenom :", font=("Segoe UI", 10, "bold"), bg="#111827", fg="#d1d5db", anchor="w").pack(fill="x", pady=2)
        self.prenom_entry = tk.Entry(self.login_frame, font=("Segoe UI", 11), bg="#1f2937", fg="white", insertbackground="white")
        self.prenom_entry.pack(fill="x", pady=5)

        tk.Label(self.login_frame, text="Mot de passe :", font=("Segoe UI", 10, "bold"), bg="#111827", fg="#d1d5db", anchor="w").pack(fill="x", pady=2)
        self.pass_entry = tk.Entry(self.login_frame, font=("Segoe UI", 11), show="*", bg="#1f2937", fg="white", insertbackground="white")
        self.pass_entry.pack(fill="x", pady=5)

        tk.Button(self.login_frame, text="Se Connecter", font=("Segoe UI", 12, "bold"), bg="#0284c7", fg="white", bd=0, cursor="hand2", command=self.login).pack(fill="x", pady=20)

        # --- FRAME DU DASHBOARD ---
        self.dashboard_frame = tk.Frame(root, bg="#0b0f19", padx=20, pady=20)

        self.welcome_label = tk.Label(self.dashboard_frame, text="Bienvenue", font=("Segoe UI", 16, "bold"), bg="#0b0f19", fg="#0284c7")
        self.welcome_label.pack(anchor="w", pady=5)

        tk.Label(self.dashboard_frame, text="Selectionnez une specialite medicale :", font=("Segoe UI", 11), bg="#0b0f19", fg="#9ca3af").pack(anchor="w", pady=5)

        # Grille des spécialités
        spec_frame = tk.Frame(self.dashboard_frame, bg="#0b0f19")
        spec_frame.pack(fill="x", pady=10)

        self.specialties = [
            ("Cardiologie", "Cardiologie", "Dr. Ben Salah", "Bureau 01"),
            ("Dentaire", "Medecine Dentaire", "Dr. Mabrouk", "Bureau 02"),
            ("Orthopedie", "Orthopedie", "Dr. Karray", "Bureau 03"),
            (" Nephrologie", "Nephrologie", "Dr. Mansouri", "Bureau 04"),
            ("Analyses", "Analyses Medicales", "Laboratoire Central", "Bureau 05"),
            ("Chirurgie", "Chirurgie Generale", "Pr. Khelil", "Bloc Chirurgical")
        ]

        self.spec_buttons = []
        for i, (txt, spec, doc, room) in enumerate(self.specialties):
            btn = tk.Button(spec_frame, text=txt, font=("Segoe UI", 10, "bold"), bg="#1f2937", fg="white", relief="solid", bd=1,
                            command=lambda s=spec, d=doc, r=room, b=i: self.select_spec(s, d, r, b))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="nsew")
            self.spec_buttons.append(btn)

        for i in range(3):
            spec_frame.columnconfigure(i, weight=1)

        # Boutons d'actions
        action_frame = tk.Frame(self.dashboard_frame, bg="#0b0f19")
        action_frame.pack(fill="x", pady=10)

        tk.Button(action_frame, text="Prendre un Ticket Live", font=("Segoe UI", 11, "bold"), bg="#16a34a", fg="white", bd=0, command=self.take_ticket).pack(side="left", expand=True, fill="x", padx=5)
        tk.Button(action_frame, text="Prendre un Rendez-vous", font=("Segoe UI", 11, "bold"), bg="#ca8a04", fg="white", bd=0, command=self.book_appointment).pack(side="right", expand=True, fill="x", padx=5)

        # --- SALLE D'ATTENTE ---
        self.hall_frame = tk.Frame(self.dashboard_frame, bg="#111827", padx=15, pady=15, bd=2, relief="groove")
        
        self.hall_title = tk.Label(self.hall_frame, text="Salle d'Attente", font=("Segoe UI", 12, "bold"), bg="#111827", fg="#38bdf8")
        self.hall_title.pack(anchor="w")

        # Écran LED
        led_box = tk.Frame(self.hall_frame, bg="black", padx=10, pady=10)
        led_box.pack(fill="x", pady=10)
        tk.Label(led_box, text="NUMERO APPELE AU GUICHET :", font=("Segoe UI", 8), bg="black", fg="#9ca3af").pack()
        self.led_label = tk.Label(led_box, text="#12", font=("Courier New", 28, "bold"), bg="black", fg="#22c55e")
        self.led_label.pack()
        self.led_doc_label = tk.Label(led_box, text="Dr. Ben Salah", font=("Segoe UI", 10, "bold"), bg="black", fg="#38bdf8")
        self.led_doc_label.pack()

        # Stats bar
        stats_frame = tk.Frame(self.hall_frame, bg="#111827")
        stats_frame.pack(fill="x", pady=5)
        
        self.stat_ahead = tk.Label(stats_frame, text="Personnes avant vous : 4", font=("Segoe UI", 10), bg="#1f2937", fg="#f3f4f6", pady=5)
        self.stat_ahead.pack(side="left", expand=True, fill="x", padx=2)
        
        self.stat_time = tk.Label(stats_frame, text="Temps estime : ~12 min", font=("Segoe UI", 10), bg="#1f2937", fg="#f3f4f6", pady=5)
        self.stat_time.pack(side="right", expand=True, fill="x", padx=2)

        # Liste des patients
        patients_frame = tk.Frame(self.hall_frame, bg="#111827")
        patients_frame.pack(fill="x", pady=10)
        
        tk.Label(patients_frame, text="PATIENTS PRESENTS DANS LA SALLE", font=("Segoe UI", 9, "bold"), bg="#111827", fg="#38bdf8").pack(anchor="w", pady=2)
        
        self.p_labels = []
        p_names = [("Mohamed", "#13"), ("Youssef", "#14"), ("Mariem", "#15"), 
                   ("Moi", "#16 (Moi)"), ("Ahmed", "#17"), ("Leila", "#18")]
        
        grid_p = tk.Frame(patients_frame, bg="#111827")
        grid_p.pack(fill="x")
        
        for idx, (name, ticket) in enumerate(p_names):
            p_box = tk.Frame(grid_p, bg="#1f2937", padx=5, pady=5, bd=1, relief="solid")
            p_box.grid(row=idx//3, column=idx%3, padx=4, pady=4, sticky="nsew")
            
            lbl = tk.Label(p_box, text=f"{name}\n{ticket}", font=("Segoe UI", 9), bg="#1f2937", fg="white")
            lbl.pack()
            self.p_labels.append(lbl)
            
        for i in range(3):
            grid_p.columnconfigure(i, weight=1)

        # Status porte
        self.door_label = tk.Label(self.hall_frame, text="Porte du Bureau : En cours d'examen...", font=("Segoe UI", 10, "bold"), bg="#030712", fg="#e2e8f0", pady=8)
        self.door_label.pack(fill="x", pady=5)

        # Box rendez-vous
        self.appt_frame = tk.Frame(self.dashboard_frame, bg="#064e3b", padx=15, pady=15, bd=1, relief="solid")
        tk.Label(self.appt_frame, text="Rendez-vous Confirme a l'Hopital", font=("Segoe UI", 12, "bold"), bg="#064e3b", fg="#34d399").pack(anchor="w")
        self.appt_details = tk.Label(self.appt_frame, text="", font=("Segoe UI", 10), bg="#064e3b", fg="#ecfdf5", justify="left")
        self.appt_details.pack(anchor="w", pady=5)

        # Déconnexion
        tk.Button(self.dashboard_frame, text="Deconnexion", font=("Segoe UI", 10), bg="#4b5563", fg="white", bd=0, command=self.logout).pack(fill="x", pady=15)

    def login(self):
        nom = self.nom_entry.get().strip()
        prenom = self.prenom_entry.get().strip()
        pwd = self.pass_entry.get().strip()

        if not nom or not prenom or not pwd:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs !")
            return

        self.user_name = f"{nom} {prenom}"
        self.p_labels[3].config(text=f"{self.user_name}\n#16 (Moi)")
        self.welcome_label.config(text=f"Bienvenue, {self.user_name}")
        
        self.login_frame.place_forget()
        self.dashboard_frame.pack(fill="both", expand=True)

    def select_spec(self, spec, doc, room, index):
        for i, btn in enumerate(self.spec_buttons):
            if i == index:
                btn.config(bg="#0369a1", fg="white")
            else:
                btn.config(bg="#1f2937", fg="white")
        
        self.selected_specialty = spec
        self.selected_doctor = doc
        self.selected_room = room

    def take_ticket(self):
        if not self.selected_specialty:
            messagebox.showwarning("Attention", "Veuillez d'abord selectionner une specialite medicale !")
            return

        self.current_called = 12
        self.my_ticket = 16
        self.hall_title.config(text=f"Salle d'Attente : {self.selected_specialty}")
        self.led_label.config(text=f"#{self.current_called}")
        self.led_doc_label.config(text=f"{self.selected_doctor} ({self.selected_room})")
        
        self.appt_frame.pack_forget()
        self.hall_frame.pack(fill="both", expand=True, pady=10)
        
        messagebox.showinfo("Succes", "Ticket pris avec succes ! Vous etes pointe dans la file d'attente.")

        if not self.running_queue:
            self.running_queue = True
            threading.Thread(target=self.update_queue, daemon=True).start()

    def update_queue(self):
        while self.current_called < self.my_ticket and self.running_queue:
            time.sleep(3)
            self.current_called += 1
            self.root.after(0, self.refresh_gui)

    def refresh_gui(self):
        self.led_label.config(text=f"#{self.current_called}")
        ahead = max(0, self.my_ticket - self.current_called - 1)
        self.stat_ahead.config(text=f"Personnes avant vous : {ahead}")
        self.stat_time.config(text=f"Temps estime : ~{ahead * 3} min")

        if self.current_called == 13:
            self.p_labels[0].config(bg="#991b1b")
        elif self.current_called == 14:
            self.p_labels[1].config(bg="#991b1b")
        elif self.current_called == 15:
            self.p_labels[2].config(bg="#991b1b")
        elif self.current_called == 16:
            self.p_labels[3].config(bg="#065f46")
            self.door_label.config(text=f"C'est votre tour ! Entrez au {self.selected_room} chez {self.selected_doctor}.")
            messagebox.showinfo("Alerte", f"C'est votre tour ! Presentez-vous au {self.selected_room}.")

    def book_appointment(self):
        if not self.selected_specialty:
            messagebox.showwarning("Attention", "Veuillez d'abord selectionner une specialite medicale !")
            return

        self.running_queue = False
        self.hall_frame.pack_forget()
        
        details = f"Specialite : {self.selected_specialty}\nMedecin/Service : {self.selected_doctor} ({self.selected_room})\nDate et Heure : Lundi 16 Novembre 2026 a 09:30"
        self.appt_details.config(text=details)
        self.appt_frame.pack(fill="x", pady=10)

    def logout(self):
        self.running_queue = False
        self.dashboard_frame.pack_forget()
        self.nom_entry.delete(0, tk.END)
        self.prenom_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)
        self.hall_frame.pack_forget()
        self.appt_frame.pack_forget()
        for btn in self.spec_buttons:
            btn.config(bg="#1f2937")
        self.selected_specialty = ""
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=450, height=400)

if __name__ == "__main__":
    root = tk.Tk()
    app = HopitalApp(root)
    root.mainloop()