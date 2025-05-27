import pytest
from sqlalchemy.orm import Session

from src.models.books import Book
from src.repositories.books import BookRepository
from src.services.books import BookService
from src.api.schemas.books import BookCreate, BookUpdate

def test_create_book(db_session: Session):
    """
    Teste la création d'un livre.
    """
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    book_in = BookCreate(
        title="Le Petit Prince",
        author="Antoine de Saint-Exupéry",
        isbn="9782070612758",
        available=True
    )

    book = service.create(obj_in=book_in)

    assert book.title == "Le Petit Prince"
    assert book.author == "Antoine de Saint-Exupéry"
    assert book.isbn == "9782070612758"
    assert book.available is True

def test_get_book(db_session: Session):
    """
    Teste la récupération d'un livre par ID.
    """
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    book_in = BookCreate(
        title="1984",
        author="George Orwell",
        isbn="9780451524935"
    )
    book = service.create(obj_in=book_in)

    retrieved = service.get(id=book.id)
    assert retrieved is not None
    assert retrieved.id == book.id
    assert retrieved.title == "1984"

def test_update_book(db_session: Session):
    """
    Teste la mise à jour d'un livre.
    """
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    book_in = BookCreate(
        title="Dune",
        author="Frank Herbert",
        isbn="9780441013593"
    )
    book = service.create(obj_in=book_in)

    book_update = BookUpdate(title="Dune (édition révisée)")
    updated = service.update(db_obj=book, obj_in=book_update)

    assert updated.id == book.id
    assert updated.title == "Dune (édition révisée)"
    assert updated.author == "Frank Herbert"

def test_get_multi_books(db_session: Session):
    """
    Teste la récupération de plusieurs livres.
    """
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    service.create(obj_in=BookCreate(title="Livre 1", author="Auteur 1", isbn="1"))
    service.create(obj_in=BookCreate(title="Livre 2", author="Auteur 2", isbn="2"))

    books = service.get_multi(skip=0, limit=10)
    assert len(books) >= 2

def test_delete_book(db_session: Session):
    """
    Teste la suppression d'un livre.
    """
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    book = service.create(obj_in=BookCreate(title="À supprimer", author="Auteur", isbn="999"))
    deleted = service.remove(id=book.id)

    assert deleted.id == book.id
    assert service.get(id=book.id) is None

def test_create_book_isbn_already_used(db_session: Session):
    """
    Teste la création d'un livre avec un ISBN déjà utilisé.
    """
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    book_in = BookCreate(
        title="Doublon",
        author="Auteur",
        isbn="1234567890"
    )
    service.create(obj_in=book_in)

    # Tentative de création avec le même ISBN
    with pytest.raises(ValueError):
        service.create(obj_in=book_in)

def test_create_book_email_already_used(db_session: Session):
    """
    Teste la création d'un livre avec un email déjà utilisé.
    """
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    book_in = BookCreate(
        title="Doublon Email",
        author="Auteur",
        isbn="0987654321",
        email="duplicate@example.com",
        password="password123",
        full_name="Duplicate User"
    )
    service.create(obj_in=book_in)

    # Tentative de création avec le même email
    with pytest.raises(ValueError):
        service.create(obj_in=book_in)

