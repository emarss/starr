from django.db import models

# Create your models here.
class Bible(models.Model):
	def get_new_testment(self):
		return {
			"Matthew" : 28,
			"Mark" : 16,
			"Luke" : 24,
			"John" : 21,
			"Acts" : 28,
			"Romans" : 16,
			"1 Corinthians" : 16,
			"2 Corinthians" : 13,
			"Galatians" : 6,
			"Ephesians" : 6,
			"Philippians" : 4,
			"Colossians" : 4,
			"1 Thessalonians" : 5,
			"2 Thessalonians" : 3,
			"1 Timothy" : 6,
			"2 Timothy" : 4,
			"Titus" : 3,
			"Philemon" : 1,
			"Hebrews" : 13,
			"James" : 5,
			"1 Peter" : 5,
			"2 Peter" : 3,
			"1 John" : 5,
			"2 John" : 1,
			"3 John" : 1,
			"Jude" : 1,
			"Revelations" : 22
		}

	def get_old_testment(self):
		return {
			"Genesis" : 50,
			"Exodus" : 40,
			"Leviticus" : 27,
			"Numbers" : 36,
			"Deuteronomy" : 34,
			"Joshua" : 24,
			"Judges" : 21,
			"Ruth" : 4,
			"1 Samuel" : 31,
			"2 Samuel" : 24,
			"1 Kings" : 22,
			"2 Kings" : 25,
			"1 Chronicles" : 29,
			"2 Chronicles" : 36,
			"Ezra" : 10,
			"Nehemiah" : 13,
			"Esther" : 10,
			"Job" : 42,
			"Psalms" : 150,
			"Proverbs" : 31,
			"Ecclesiastes" : 12,
			"Songs of Solomon" : 8,
			"Isaiah" : 66,
			"Jeremiah" : 52,
			"Lamentations" : 5,
			"Ezekiel" : 48,
			"Daniel" : 12,
			"Hosea" : 14,
			"Joel" : 3,
			"Amos" : 9,
			"Obadiah" : 1,
			"Jonah" : 4,
			"Micah" : 7,
			"Nahum" : 3,
			"Habakkuk" : 3,
			"Zephaniah" : 3,
			"Haggai" : 2,
			"Zechariah" : 14,
			"Malachi" : 4
		}

	def get_all_bibles(self):
		bibles = self.get_old_testment()
		nt = self.get_new_testment()
		bibles.update(nt)
		return bibles
	def get_all_bibles_list(self):
		b_dict = list(self.get_all_bibles().keys())
		b_list = []
		for i in range(0, len(b_dict)):
			b = (b_dict[i], b_dict[i])
			b_list.append(b)
		return b_list

