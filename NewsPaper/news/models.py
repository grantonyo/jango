from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


# Модель Author
# Модель, содержащая объекты всех авторов.
# Имеет следующие поля:
#         cвязь «один к одному» с встроенной моделью пользователей User;
#         рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать.

# Метод update_rating() модели Author, который обновляет рейтинг пользователя, переданный в аргумент этого метода.
# Он состоит из следующего:
#     суммарный рейтинг каждой статьи автора умножается на 3;
#     суммарный рейтинг всех комментариев автора;
#     суммарный рейтинг всех комментариев к статьям автора.

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.authorUser.username


    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        post_list = Post.objects.filter(author=self, categoryType='AR')
        cArtRat = 0
        for i in post_list:
            i.comment_set.aggregate(commentArtRating=Sum('rating'))
            cArtRat += i.get('commentArtRating')

        self.ratingAuthor = pRat*3+cRat+cArtRat
        self.save()


# Модель Category
# Категории новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.).
# Имеет единственное поле: название категории. Поле должно быть уникальным
# (в определении поля необходимо написать параметр unique = True).
class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name.title()


# Модель Post
# Эта модель должна содержать в себе статьи и новости, которые создают пользователи.
# Каждый объект может иметь одну или несколько категорий.
# Соответственно, модель должна включать следующие поля:
#         связь «один ко многим» с моделью Author;
#         поле с выбором — «статья» или «новость»;
#         автоматически добавляемая дата и время создания;
#         связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
#         заголовок статьи/новости;
#         текст статьи/новости;
#         рейтинг статьи/новости.

# Методы like() и dislike() в моделях Comment и Post, которые увеличивают/уменьшают рейтинг на единицу.
# Метод preview() модели Post, который возвращает начало статьи (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце.


NEWS = "NW"
ARTICLE = 'AR'
CATEGORY_CHOICES = (
    (NEWS, 'Новость'),
    (ARTICLE, 'Статья'),
)

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'ID: {self.id} | {self.title}'

    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:20]+'...'



# Модель PostCategory
# Промежуточная модель для связи «многие ко многим»:
#         связь «один ко многим» с моделью Post;
#         связь «один ко многим» с моделью Category.
class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'ID:{self.postThrough.id} | {self.categoryThrough.name}'

# Модель Comment
# Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже.
# Модель будет иметь следующие поля:
#         связь «один ко многим» с моделью Post;
#         связь «один ко многим» со встроенной моделью User
#         (комментарии может оставить любой пользователь, необязательно автор);
#         текст комментария;
#         дата и время создания комментария;
#         рейтинг комментария.

# Методы like() и dislike() в моделях Comment и Post, которые увеличивают/уменьшают рейтинг на единицу.

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'[ID статьи: {self.commentPost.id}] {self.commentUser.username}: {self.text[:100]}'

    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

