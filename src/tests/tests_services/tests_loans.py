import pytest
from sqlalchemy.orm import Session

from src.models.loans import Loan
from src.models.users import User
from src.models.books import Book
from src.repositories.loans import LoanRepository
from src.services.loans import LoanService
from src.api.schemas.loans import LoanCreate, LoanUpdate
from src.api.schemas.users import UserCreate
from src.api.schemas.books import BookCreate

def create_user_and_book(db_session):
    # Crée un utilisateur et un livre pour les tests de prêt
    from src.repositories.users import UserRepository
    from src.services.users import UserService
    from src.repositories.books import BookRepository
    from src.services.books import BookService

    user_repo = UserRepository(User, db_session)
    user_service = UserService(user_repo)
    user = user_service.create(obj_in=UserCreate(
        email="loanuser@example.com",
        password="password123",
        full_name="Loan User"
    ))

    book_repo = BookRepository(Book, db_session)
    book_service = BookService(book_repo)
    book = book_service.create(obj_in=BookCreate(
        title="Book for Loan",
        author="Author",
        isbn="LOAN123"
    ))

    return user, book

def test_create_loan(db_session: Session):
    """
    Teste la création d'un prêt.
    """
    user, book = create_user_and_book(db_session)
    repository = LoanRepository(Loan, db_session)
    service = LoanService(repository)

    loan_in = LoanCreate(
        user_id=user.id,
        book_id=book.id
    )

    loan = service.create(obj_in=loan_in)

    assert loan.user_id == user.id
    assert loan.book_id == book.id
    assert loan.returned is False

def test_get_loan(db_session: Session):
    """
    Teste la récupération d'un prêt par ID.
    """
    user, book = create_user_and_book(db_session)
    repository = LoanRepository(Loan, db_session)
    service = LoanService(repository)

    loan = service.create(obj_in=LoanCreate(user_id=user.id, book_id=book.id))
    retrieved = service.get(id=loan.id)
    assert retrieved is not None
    assert retrieved.id == loan.id

def test_update_loan(db_session: Session):
    """
    Teste la mise à jour d'un prêt (ex : retour du livre).
    """
    user, book = create_user_and_book(db_session)
    repository = LoanRepository(Loan, db_session)
    service = LoanService(repository)

    loan = service.create(obj_in=LoanCreate(user_id=user.id, book_id=book.id))
    loan_update = LoanUpdate(returned=True)
    updated = service.update(db_obj=loan, obj_in=loan_update)

    assert updated.id == loan.id
    assert updated.returned is True

def test_get_multi_loans(db_session: Session):
    """
    Teste la récupération de plusieurs prêts.
    """
    user, book = create_user_and_book(db_session)
    repository = LoanRepository(Loan, db_session)
    service = LoanService(repository)

    service.create(obj_in=LoanCreate(user_id=user.id, book_id=book.id))
    service.create(obj_in=LoanCreate(user_id=user.id, book_id=book.id))

    loans = service.get_multi(skip=0, limit=10)
    assert len(loans) >= 2

def test_delete_loan(db_session: Session):
    """
    Teste la suppression d'un prêt.
    """
    user, book = create_user_and_book(db_session)
    repository = LoanRepository(Loan, db_session)
    service = LoanService(repository)

    loan = service.create(obj_in=LoanCreate(user_id=user.id, book_id=book.id))
    deleted = service.remove(id=loan.id)

    assert deleted.id == loan.id
    assert service.get(id=loan.id) is None

def test_create_loan_already_exists(db_session: Session):
    """
    Teste la création d'un prêt déjà existant (ex : même livre non rendu).
    """
    user, book = create_user_and_book(db_session)
    repository = LoanRepository(Loan, db_session)
    service = LoanService(repository)

    loan_in = LoanCreate(user_id=user.id, book_id=book.id)
    service.create(obj_in=loan_in)

    # Tentative de création d'un prêt pour le même livre non rendu
    with pytest.raises(ValueError):
        service.create(obj_in=loan_in)