from PyQt6.QtWidgets import QMainWindow
from pkg_resources import non_empty_lines

from gui import *
import csv

class Logic(QMainWindow, Ui_MainWindow):
    """
    main class used for the logic of the voting ballot program
    """
    def __init__(self) -> None:
        """
        initializes the program, this connects the next button to the correct page while making sure that radiobuttons are set up correctly
        """
        super().__init__()
        self.setupUi(self)
        # next button connection
        self.pushButton_wlc_nxt_btn.clicked.connect(self.voter_id_check_wlc_pg)
        self.pushButton_prty_pg_next.clicked.connect(self.party_page_check)
        self.pushButton_cnd_sel_nxt.clicked.connect(self.candidate_page_check)
        self.pushButton_ty_pg_sbt.clicked.connect(self.ty_pg_sbmt_rtrn)

        # initial information
        self.voter_id = None
        self.prty = None
        self.cnd = None

        # initial first page
        self.welcome_page.show()
        self.party_page.hide()
        self.candidate_page.hide()
        self.thank_you_page.hide()
        # Group them so only one can be selected
        ##self.button_group = QButtonGroup(self)
        #self.button_group.addButton(radio1)
       # self.button_group.addButton(radio2)
        #self.button_group.addButton(radio3)

    def reset(self, group: QtWidgets.QButtonGroup) -> None:
        """
        method that allows the program to properly be reset
        """
        # Temporarily allow no selection, uncheck all, then restore exclusivity
        group.setExclusive(False)
        for b in group.buttons():
            b.setChecked(False)
        group.setExclusive(True)




    def voter_id_check_wlc_pg(self) -> int:
        """
        welcome page; ensuring that advancement can only be made when conditions are met
        returns:
            self.voter_id
        """
        self.voter_id = self.lineEdit_id_number.text().strip()
        try:
            self.voter_id = int(self.voter_id)
            self.label_wlc_error.setText(" ")
            self.welcome_page.hide()
            self.party_page.show()

        except ValueError:
            self.label_wlc_error.setText('Only numbers are accepted')
        self.lineEdit_id_number.clear()
        return self.voter_id

    def party_page_check(self) -> str:
        """
        party page, ensuring that advancment to next page can only be done when a party is selected.
        returns:
            error text and self.prty

        """
        self.prty = None
        if self.radioButton_ind.isChecked():
            self.prty = "Indepandent"
        elif self.radioButton_na.isChecked():
            self.prty = "N/A"
        elif self.radioButton_dem.isChecked():
            self.prty = "Democrat"
        elif self.radioButton_rep.isChecked():
            self.prty = "Republican"
        else:

            self.lbl_prty_pg_err.setText("Must be filled out before continuing")
            return

        self.lbl_prty_pg_err.setText(" ")

        self.party_page.hide()
        self.candidate_page.show()


        return self.prty

    def candidate_page_check(self) -> str:
        """
        marks and saves the selected information by the user

        returns:
            self.cnd

        """
        self.cnd = None
        if self.radioButton_jim_cle_cnd.isChecked():
            self.cnd = "John D. Smith"
        elif self.radioButton_jhn_smith_cnd.isChecked():
            self.cnd = "Jim R. Cole"
        else:
            self.label_cand_pg_err.setText("Fill out before proceeding")
            return

        self.label_cand_pg_err.setText(" ")
        self.candidate_page.hide()
        self.thank_you_page.show()

        self.radioButton_jhn_smith_cnd.setChecked(False)
        self.radioButton_jim_cle_cnd.setChecked(False)
        return self.cnd

    def ty_pg_sbmt_rtrn(self) -> None:
        """
        submits the information gathered then stores in csv file, revertcs back to home page while also resetting.

        """
        with open('data.csv', 'a', newline = '') as csvfile:
            content = csv.writer(csvfile)
            content.writerow([self.voter_id, self.prty, self.cnd])



        self.thank_you_page.hide()
        self.party_page.hide()
        self.candidate_page.hide()
        self.welcome_page.show()
        self.reset(self.party_group)
        self.reset(self.candidate_group)




