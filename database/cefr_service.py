CEFR_A1_ID = 1
CEFR_A2_ID = 2
CEFR_B1_ID = 3
CEFR_B2_ID = 4
CEFR_C2_ID = 5

class CerfService:
  @staticmethod
  def get_id_by_string(value: str):
    if value == "a1":
      return CEFR_A1_ID
    elif value == "a2":
      return CEFR_A2_ID
    elif value == "b1":
      return CEFR_B1_ID
    elif value == "b2":
      return CEFR_B2_ID
    elif value == "c1":
      return CEFR_C2_ID