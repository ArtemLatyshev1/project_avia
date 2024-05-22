from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.responses import JSONResponse
from starlette import status
from models.good import *
from sqlalchemy.orm import sessionmaker, Session
from public.db import engine_s


def get_session():
     with Session(engine_s) as session:
         try:
           yield session
         finally:
           session.close()
#реализация маршрутов для операций c конкретными тегами - конкретизация роутера

tickets_router = APIRouter(tage=[Tags.tickets])

#получить билет по id пользователя
@tickets_router.get("/{id}", response_model=Union[New_Respons, Main_Ticket], tags=[Tags.tickets])
# далее идут операции пути для CRUD
def get_ticket_(id: int, DB: Session = Depends(get_session)):
    '''
    получаем билет по id
    '''
    ticket = DB.query(Ticket).filter(Ticket.id == id).first()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if ticket == None:
        return JSONResponse(status_code=404, content={"message": "Билет не найден"})
    # если билет найден, отправляем его
    else:
        return ticket

@tickets_router.get("/", response_model=Union[list[Main_Ticket], New_Respons], tags=[Tags.tickets])
def get_user_db(DB: Session = Depends(get_session)):
    '''
    получаем все билеты
    '''
    tickets = DB.query(Ticket).all()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if tickets == None:
        return JSONResponse(status_code=404, content={"message": "Пользователи не найдены"})
    return tickets

@tickets_router.post("/", response_model=Union[Main_Ticket, New_Respons], tags=[Tags.tickets], status_code=status.HTTP_201_CREATED)
def create_user(item: Annotated[Main_Ticket, Body(embed=True, description="Новый билет")],
                DB: Session = Depends(get_session)):
    try:
      ticket = User(name_person_ticket=item.name_person_ticket, to_go=item.to_go, price=item.price)

      if ticket is None:
          raise HTTPException(status_code=404, detail="Объект не определен")
      DB.add(ticket)
      DB.commit()
      DB.refresh(ticket)
      return ticket
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта {ticket}")


@tickets_router.put("/", response_model=Union[Main_Ticket, New_Respons], tags=[Tags.tickets])
def edit_user_(item: Annotated[Main_Ticket,Body(embed=True, description="Изменяем данные для билета пользователя по его id")],
               DB: Session = Depends(get_session)):
    # получаем пользователя по id
    ticket = DB.query(Ticket).filter(Ticket.id == item.id).first()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if ticket == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    # если пользователь найден, изменяем его данные и отправляем обратно клиенту
    ticket.name_person_ticket = item.name_person_ticket
    try:
        DB.commit()
        DB.refresh(ticket)  # сохраняем изменения
    except HTTPException:
        return JSONResponse(status_code=404, content={"message": ""})
    return ticket

@tickets_router.delete("/{id}", response_class=JSONResponse, tags=[Tags.tickets])
def delete_user(id: int, DB: Session = Depends(get_session)):
    # получаем пользователя по id
    ticket = DB.query(Ticket).filter(Ticket.id == id).first()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if ticket == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    try:
        DB.delete(ticket)
        DB.commit()  # сохраняем изменения
    except HTTPException:
        JSONResponse(content={'message' : f'Ошибка'})
    return JSONResponse(content={'message' : f'Билет удалён {id}'})
