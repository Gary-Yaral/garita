from database import vehicles

def findPlateInDB(plate_number):
  if plate_number in vehicles.keys():
    return (True, vehicles[plate_number])
  return (False, {"error": "Plate number not found"})