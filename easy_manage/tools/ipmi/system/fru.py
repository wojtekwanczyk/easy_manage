"Class for fetching data from FRU (BMC/motherboard in this case)"


class FRUInventoryOwner:
    "Base class for FRU inventory utilization"

    def __init__(self, ipmi):
        self.ipmi = ipmi
        self.fru_inventory = None

    def _fetch_inventory(self):
        "Method which fetches data from the fru inventory"
        self.fru_inventory = self.ipmi.get_fru_inventory()


class FRU(FRUInventoryOwner):
    "Class for easier access to FRU data"

    def board_info(self):
        "General board info"
        if not self.fru_inventory:
            self._fetch_inventory()
        if self.fru_inventory.board_info_area:
            return {
                "manufacturer": self.fru_inventory.board_info_area.manufacturer,
                "product_name": self.fru_inventory.board_info_area.product_name,
                "serial_number": self.fru_inventory.board_info_area.serial_number,
                "part_number": self.fru_inventory.board_info_area.part_number,
                "fru_file_id": self.fru_inventory.board_info_area.fru_file_id}
        return None

    def product_info(self):
        "General product info"
        if not self.fru_inventory:
            self._fetch_inventory()
        if self.fru_inventory.product_info_area:
            return{
                "manufacturer": self.fru_inventory.product_info_area.manufacturer,
                "name": self.fru_inventory.product_info_area.name,
                "part_number": self.fru_inventory.product_info_area.part_number,
                "version": self.fru_inventory.product_info_area.version,
                "serial_number": self.fru_inventory.product_info_area.serial_number,
                "asset_tag": self.fru_inventory.product_info_area.asset_tag}
        return None


class FRUChassis(FRUInventoryOwner):
    "Class for accessing fru chassis data "

    def chassis_info(self):
        "Chassis info. Type field meaning can be found in pyipmi/fru.py"
        if not self.fru_inventory:
            self._fetch_inventory()
        if self.fru_inventory.chassis_info_area:
            return {
                "type": self.fru_inventory.chassis_info_area.type,
                "part_number": self.fru_inventory.chassis_info_area.part_number,
                "serial_number": self.fru_inventory.chassis_info_area.serial_number
            }
        return None
