import customtkinter as ctk
import subprocess

class LoginSignupApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login or Signup")
        self.geometry("400x300")
        self.configure(bg_color="lightblue")  # Set a background color

        # Configure the main label
        self.label = ctk.CTkLabel(self, text="Welcome! Please log in or sign up.", font=("Roboto", 20, "bold"), text_color="white")
        self.label.pack(pady=30)

        # Configure the login button
        self.login_button = ctk.CTkButton(self, text="Log In", command=self.go_to_login, 
                                          font=("Roboto", 14), fg_color="green", hover_color="darkgreen", text_color="white")
        self.login_button.pack(pady=15, ipadx=10, ipady=5)

        # Configure the signup button
        self.signup_button = ctk.CTkButton(self, text="Sign Up", command=self.go_to_signup, 
                                           font=("Roboto", 14), fg_color="blue", hover_color="darkblue", text_color="white")
        self.signup_button.pack(pady=15, ipadx=10, ipady=5)

    def go_to_login(self):
        # Redirect to the login page
        subprocess.run(["python", "C:\\Users\\dell\\OneDrive\\Documents\\2nd Year\\4th Sem\\DSA\\DSA PROJECT\\home_page.py"])

    def go_to_signup(self):
        # Redirect to the signup page
        subprocess.run(["python", "signup.py"])

if __name__ == "__main__":
    app = LoginSignupApp()
    app.mainloop()
