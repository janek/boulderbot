from gyms import check, gyms, GymName

def test_gyms():
  for gym in GymName:
      check(gym)
