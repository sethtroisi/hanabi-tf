from card_deck import *

import unittest

class TestStringMethods(unittest.TestCase):

  def test_card_machesNumberAndColor(self):
      blueTwo = Card(Card.COLORS[2], Card.NUMBERS[1])
      self.assertTrue(blueTwo.matchesColor(3))
      self.assertTrue(blueTwo.matchesNumber(2))

      self.assertFalse(blueTwo.matchesColor(5))
      self.assertFalse(blueTwo.matchesNumber(5))


  def test_card_machesNumberAndColor(self):
      blueTwo = Card(Card.COLORS[2], Card.NUMBERS[1])
      redThree = Card(Card.COLORS[3], Card.NUMBERS[2])

      self.assertEqual(blueTwo, blueTwo)
      self.assertNotEqual(blueTwo, redThree)

      self.assertTrue(blueTwo < redThree)
      self.assertTrue(redThree > blueTwo)


  def test_deck_hasAllCards(self):
      d1 = Deck(1)
      cards = [d1.draw() for i in range(len(Card.COLORS) * len(Card.NUMBERS))]
      assert len(cards) == 25
      assert len(set(cards)) == 25
      

  def test_deck_hasUniqueHashes(self):
      d1 = Deck(1)
      cards = [hash(d1.draw()) for i in range(len(Card.COLORS) * len(Card.NUMBERS))]
      assert len(cards) == 25
      assert len(set(cards)) == 25


  def test_deck_getState(self):
      a = Deck(1)
      b = Deck(1)
      c = Deck(2)
      for i in range(25):
        assert a.getState() == b.getState()
        assert a.getState() != c.getState()
        assert a.draw() == b.draw()

  def test_deck_setState(self):
      a = Deck(1)

      front = tuple(a.draw() for i in range(10))
      saveState = a.getState()

      back = tuple(a.draw() for i in range(10))
      assert front != back

      a.setState(saveState)
      secondBack = tuple(a.draw() for i in range(10))
      assert back == secondBack
      
      a.reset()
      secondFront = tuple(a.draw() for i in range(10))
      assert front == secondFront



if __name__ == '__main__':
    unittest.main(exit=False)
