from django.db import models

class TimeStampModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract= True #don't create table in db


class Category(TimeStampModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering =["name"]

class Tag(TimeStampModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(TimeStampModel):
    STATUS_CHOICES =[("active", "Active"),
                     ("in_active", "Inactive"),
                     ]                    
    title = models.CharField(max_length=200)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="post_images/%Y/%m/%d", blank=False)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES , default="active")
    views_count = models.PositiveBigIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
    
class Contact(TimeStampModel):
    message = models.TextField()
    name = models.CharField(max_length=100)
    email =models.EmailField()
    subject = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ["created_at"]   
class UserProfile(TimeStampModel):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="user_image/%Y/%m/%d", blank=False)
    address= models.CharField(max_length=200)
    biography = models.TextField()

    def __str__(self):                                          #if there id 1to1 then u can write direct that model
        return self.user.username                               # if there is a forghenkey then u have to write modelname_set
    
class Comment(TimeStampModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f"{self.email} | {self.comment[:70]}"
    
class NewsLetter(TimeStampModel):
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.email
