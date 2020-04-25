from django.contrib.auth.models import User
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


class BibleHistory(models.Model):
	bible_book		= models.CharField(max_length=50)
	bible_chapter	= models.CharField(max_length=50)
	user			= models.ForeignKey(User, on_delete=models.CASCADE)
	created_at		= models.DateTimeField(auto_now=True)
	updated_at		= models.DateTimeField(auto_now_add=True)

	def save_model(form, request):
		entry = BibleHistory()
		entry.user = request.user
		entry.bible_book = form.cleaned_data['bible_book']
		entry.bible_chapter = form.cleaned_data['bible_chapter']
		entry.save()
		return True


class BibleComment(models.Model):
	verse_ref		= models.CharField(max_length=50)
	comment			= models.TextField()
	user			= models.ForeignKey(User, on_delete=models.CASCADE)
	created_at		= models.DateTimeField(auto_now=True)
	updated_at		= models.DateTimeField(auto_now_add=True)
	
	def save_model(form, request):
		comment = BibleComment()
		comment.user = request.user
		comment.comment = form.cleaned_data['comment']
		comment.verse_ref = form.cleaned_data['verse_ref']
		comment.save()
		return True

	def update_model(form, request):
		try:
			comment = BibleComment.objects.get(id=request.POST["comment_id"])
		except BibleComment.DoesNotExist:
			return True
		comment.comment = form.cleaned_data['comment_edit']
		comment.save()
		return True

	def get_comments(verse_ref, request):
		return BibleComment.objects.filter(
				user= request.user,
				verse_ref = verse_ref
			)

	def delete_comment(verse_ref, request):
		try:
			comment = BibleComment.objects.get(
						id = request.POST["comment_id"]
					);
		except BibleComment.DoesNotExist:
			return True	
		comment.delete()
		return True

class BibleNotebook(models.Model):
	notes			= models.TextField(null=True, blank=True)
	user			= models.ForeignKey(User, on_delete=models.CASCADE)
	created_at		= models.DateTimeField(auto_now=True)
	updated_at		= models.DateTimeField(auto_now_add=True)

	def save_model(form, request):
		try:
			notebook = BibleNotebook.objects.get(user=request.user)
		except BibleNotebook.DoesNotExist:
			notebook = BibleNotebook()
			notebook.user = request.user		
		notebook.notes = form.cleaned_data['notes']
		notebook.save()
		return True

	def get_notes(request):
		return BibleNotebook.objects.get(
				user= request.user
			)

class BibleBookmark(models.Model):
	key		= models.TextField(null=True, blank=True)
	user	= models.ForeignKey(User, on_delete=models.CASCADE)

	def process(request, key):
		try:
			notebook = BibleBookmark.objects.get(user=request.user, key=key)
			notebook.delete()
			return "removed"
		except BibleBookmark.DoesNotExist:
			notebook = BibleBookmark()
			notebook.user = request.user		
			notebook.key = key
			notebook.save()
			return "added"

	def get_bookmarks(request, chapter):
		return BibleBookmark.objects.filter(
				user= request.user,
				key__startswith= chapter
			).values("key")