import unittest

from logger import CSLogger

class LoggerTests(unittest.TestCase):

    def testCanConnectAndGetServerSheet(self):
        use_gdrive = True
        ss_name = "Logging"
        worksheet_name = "CentralSwitch"
        logger = CSLogger(use_gdrive, ss_name, worksheet_name)

        self.assertIsNotNone(logger.sheet) 
        self.assertIsNotNone(logger.client) 

        #garage_logger = CSLogger(use_gdrive, "Logging", "GarageDoors")

    def testCanConnectAndGetDoorSheet(self):
        use_gdrive = True
        ss_name = "Logging"
        worksheet_name = "GarageDoors"
        logger = CSLogger(use_gdrive, ss_name, worksheet_name)

        self.assertIsNotNone(logger.sheet) 
        self.assertIsNotNone(logger.client) 

       
    def testCanLogToServerSheet(self):
        use_gdrive = True
        ss_name = "Logging"
        worksheet_name = "CentralSwitch"
        logger = CSLogger(use_gdrive, ss_name, worksheet_name)

        self.assertIsNotNone(logger.sheet) 
        self.assertIsNotNone(logger.client) 

        num_rows = logger.sheet.row_count
        print num_rows
        logger.log(["CentralStation", "logging test executed"])
        self.assertEqual(logger.sheet.row_count, num_rows + 1)

    def testCanLogToGarageSheet(self):
        use_gdrive = True
        ss_name = "Logging"
        worksheet_name = "GarageDoors"
        logger = CSLogger(use_gdrive, ss_name, worksheet_name)

        self.assertIsNotNone(logger.sheet) 
        self.assertIsNotNone(logger.client) 

        num_rows = logger.sheet.row_count
        print num_rows
        logger.log(["test", "test name", "test" + '=>' + "test"])
        self.assertEqual(logger.sheet.row_count, num_rows + 1)

        #logger.client.get_spreadsheets_feed()


def main():
    unittest.main()

if __name__ == '__main__':
    main()