import pytest
from main import BooksCollector
# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_genre, который нам возвращает метод get_books_genre, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

@pytest.fixture
def new_collector():
    return BooksCollector()

@pytest.fixture
def collector_with_books():
    collector = BooksCollector()
    books = [
        ("1984", "Фантастика"),
        ("Мастер и Маргарита", "Фантастика"),
        ("Оно", "Ужасы"),
        ("Ну, погоди!", "Мультфильмы")
    ]
    for name, genre in books:
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
    return collector

@pytest.fixture
def collector_with_favorites(collector_with_books):
    collector = collector_with_books
    collector.add_book_in_favorites("1984")
    collector.add_book_in_favorites("Ну, погоди!")
    return collector

    def test_add_new_book_valid_name_adds_book(self, new_collector):
        new_collector.add_new_book("Война и мир")
        assert "Война и мир" in new_collector.books_genre

    @pytest.mark.parametrize(
        "name",
        [
            "",
            "Очень длинное название книги, которое превышает лимит в 40 символов",  # >40 символов
        ],
    )
    def test_add_new_book_invalid_name_does_not_add(self, new_collector, name):
        new_collector.add_new_book(name)
        assert name not in new_collector.books_genre

    def test_add_new_book_duplicate_not_added(self, new_collector):
        new_collector.add_new_book("1984")
        new_collector.add_new_book("1984")
        assert len(new_collector.get_books_genre()) == 1

    def test_set_book_genre_valid_genre(self, collector_with_books):
        collector_with_books.set_book_genre("Мастер и Маргарита", "Фантастика")
        assert collector_with_books.get_book_genre("Мастер и Маргарита") == "Фантастика"

    def test_set_book_genre_invalid_genre(self, collector_with_books):
        collector_with_books.set_book_genre("Мастер и Маргарита", "Роман")
        assert collector_with_books.get_book_genre("Мастер и Маргарита") == ""

    def test_get_book_genre_returns_correct_genre(self, collector_with_books):
        assert collector_with_books.get_book_genre("1984") == "Фантастика"
        assert collector_with_books.get_book_genre("Оно") == "Ужасы"
        assert collector_with_books.get_book_genre("Мастер и Маргарита") == ""

    def test_get_books_with_specific_genre(self, collector_with_books):
        assert collector_with_books.get_books_with_specific_genre("Фантастика") == ["1984"]
        assert collector_with_books.get_books_with_specific_genre("Ужасы") == ["Оно"]
        assert collector_with_books.get_books_with_specific_genre("Мультфильмы") == ["Ну, погоди!"]

    def test_get_books_for_children_excludes_age_rated_books(self, collector_with_books):
        children_books = collector_with_books.get_books_for_children()
        assert "Ну, погоди!" in children_books
        assert "Оно" not in children_books

    def test_add_book_in_favorites_adds_only_if_in_books_genre(self, collector_with_books):
        collector_with_books.add_book_in_favorites("Мастер и Маргарита")
        collector_with_books.add_book_in_favorites("Несуществующая книга")
        assert "Мастер и Маргарита" in collector_with_books.favorites
        assert "Несуществующая книга" not in collector_with_books.favorites

    def test_delete_book_from_favorites_removes_book(self, collector_with_favorites):
        collector_with_favorites.delete_book_from_favorites("1984")
        assert "1984" not in collector_with_favorites.favorites

    def test_get_list_of_favorites_books_returns_all_favorites(self, collector_with_favorites):
        favorites = collector_with_favorites.get_list_of_favorites_books()
        assert sorted(favorites) == sorted(["1984", "Ну, погоди!"])