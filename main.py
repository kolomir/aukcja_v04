import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QColor
from datetime import datetime
from main_ui import Ui_MainWindow  # Import szablonu UI


class AuctionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Połączenie z bazą danych
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Zmień na swoje hasło
            database="auction_db2"
        )
        self.cursor = self.db.cursor(dictionary=True)

        # Timer dla odświeżania czasu
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_selected_item_time)
        self.timer.start(1000)  # Aktualizacja co sekundę

        # Połącz sygnały
        self.ui.item_list.currentItemChanged.connect(self.display_auction_details)
        self.ui.bid_button.clicked.connect(self.place_bid)

        self.current_auction = None  # Wybrany przedmiot
        self.load_auctions()

        # Wybierz pierwszy element na liście po uruchomieniu
        if self.ui.item_list.count() > 0:
            self.ui.item_list.setCurrentRow(0)

    def load_auctions(self):
        """Załaduj listę aukcji, posortowaną według czasu do zakończenia."""
        self.ui.item_list.clear()
        self.cursor.execute("""
            SELECT *, TIMESTAMPDIFF(SECOND, NOW(), end_time) AS time_left 
            FROM auctions 
            ORDER BY 
                CASE WHEN status = 'active' THEN 1 ELSE 2 END, 
                time_left ASC
        """)
        auctions = self.cursor.fetchall()
        for auction in auctions:
            item = QListWidgetItem(auction["item_name"])
            if auction["status"] == "closed":
                item.setForeground(QColor("red"))
            self.ui.item_list.addItem(item)

    def display_auction_details(self):
        """Wyświetl szczegóły wybranego przedmiotu."""
        current_item = self.ui.item_list.currentItem()
        if not current_item:
            self.current_auction = None
            self.clear_details()
            return

        item_name = current_item.text()
        self.cursor.execute("SELECT * FROM auctions WHERE item_name=%s", (item_name,))
        auction = self.cursor.fetchone()

        if not auction:
            self.current_auction = None
            self.clear_details()
            return

        self.current_auction = auction

        # Wyświetl obraz
        pixmap = QPixmap(auction["image_path"])
        if not pixmap.isNull():
            self.ui.image_label.setPixmap(pixmap.scaled(
                self.ui.image_label.size(),  # Rozmiar docelowy
                Qt.KeepAspectRatio,         # Zachowanie proporcji
                Qt.SmoothTransformation     # Wygładzanie obrazu
            ))
        else:
            self.ui.image_label.setText("<Brak zdjęcia>")

        # Wyświetl szczegóły
        self.ui.text_opis.setText(auction["description"])
        self.ui.price_label.setText(f"Cena: {auction['current_price']} zł")
        self.ui.bid_increment_label.setText(f"Krok licytacji: {auction['auction_step']} zł")
        self.update_time_left(auction)
        self.ui.koniec_lab.setText(f"Koniec licytacji: {auction['end_time']}")

    def format_time_left(self, time_left):
        """Formatuj czas jako dni, godziny, minuty i sekundy."""
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if days > 0:
            return f"{days}d {hours}h {minutes}m {seconds}s"
        elif hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    def update_time_left(self, auction):
        """Aktualizuj czas do końca aukcji."""
        end_time = auction["end_time"]
        now = datetime.now()
        time_left = end_time - now

        if time_left.total_seconds() > 0:
            formatted_time = self.format_time_left(time_left)
            self.ui.time_left_label.setText(f"Czas do końca: {formatted_time}")
        else:
            self.ui.time_left_label.setText("Aukcja zakończona")
            if auction["status"] != "closed":
                self.close_auction(auction["id"])

    def update_selected_item_time(self):
        """Odśwież czas dla wybranego przedmiotu."""
        if self.current_auction:
            self.update_time_left(self.current_auction)

    def place_bid(self):
        """Obsłuż licytację."""
        current_item = self.ui.item_list.currentItem()
        if not current_item:
            return

        item_name = current_item.text()
        self.cursor.execute("SELECT * FROM auctions WHERE item_name=%s", (item_name,))
        auction = self.cursor.fetchone()

        if not auction:
            return

        if auction["status"] == "closed":
            self.show_error_message("Nie można licytować zakończonej aukcji.")
            return

        bidder_name = self.ui.name_input.text().strip()
        if not bidder_name:
            self.show_error_message("Wprowadź swoje imię i nazwisko.")
            return

        # Aktualizacja ceny
        new_price = auction["current_price"] + auction["auction_step"]

        # Zapisanie danych o licytacji
        now = datetime.now()
        self.cursor.execute(
            "INSERT INTO bids (auction_id, bidder_name, bid_time, bid_amount) VALUES (%s, %s, %s, %s)",
            (auction["id"], bidder_name, now, new_price)
        )
        self.cursor.execute(
            "UPDATE auctions SET current_price=%s WHERE id=%s", (new_price, auction["id"])
        )
        self.db.commit()

        self.ui.price_label.setText(f"Cena: {new_price} zł")
        self.ui.name_input.clear()

    def close_auction(self, auction_id):
        """Zamknij aukcję."""
        self.cursor.execute("UPDATE auctions SET status='closed' WHERE id=%s", (auction_id,))
        self.db.commit()
        self.load_auctions()

    def clear_details(self):
        """Wyczyść szczegóły wybranego przedmiotu."""
        self.ui.image_label.clear()
        self.ui.text_opis.clear()
        self.ui.price_label.setText("Cena: -")
        self.ui.bid_increment_label.setText("Krok licytacji: -")
        self.ui.time_left_label.setText("Czas do końca: -")

    def show_error_message(self, message):
        """Wyświetl komunikat błędu."""
        error_box = QMessageBox(self)
        error_box.setIcon(QMessageBox.Warning)
        error_box.setWindowTitle("Błąd")
        error_box.setText(message)
        error_box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuctionApp()
    window.show()
    sys.exit(app.exec_())
