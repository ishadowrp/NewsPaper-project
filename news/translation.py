from .models import Category, Post, Author
from modeltranslation.translator import register, TranslationOptions  # импортируем декоратор для перевода и класс настроек, от

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', )  # указываем, какие именно поля надо переводить в виде кортежа

@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'text', )  # указываем, какие именно поля надо переводить в виде кортежа

@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('name', )  # указываем, какие именно поля надо переводить в виде кортежа
