# Lab Report: Implementing 3 SOLID Principles (SRP, OCP, DIP)

## Goal

Implement three SOLID principles in a simple project. This project showcases:

- SRP — Single Responsibility Principle
- OCP — Open/Closed Principle
- DIP — Dependency Inversion Principle

The code lives in:
- `models.py` — data models: `Student`, `Post`
- `notifiers.py` — abstraction `Notifier` and concrete notifiers: `EmailNotifier`, `SMSNotifier`, `PushNotifier`, `NullNotifier`, `CompositeNotifier`
- `main.py` — `Forum` orchestrator and demo `main()`

---

## Single Responsibility Principle (SRP)

Theory (what/why):
- Each class/module should have exactly one reason to change.
- Keeps code easy to understand, test, and maintain.

Implementation in this project (how):
- `Student` stores only identity/contact data (name, email, phone).
- `Post` stores only post data (author + content).
- Each notifier handles only its channel-specific behavior:
	- `EmailNotifier` → email
	- `SMSNotifier` → SMS
	- `PushNotifier` → push
	- `NullNotifier` → no-op (useful for tests/silencing)
- `Forum` focuses on forum operations (create/list posts) and delegates notifications.

Result:
- Changes in email/SMS/push behavior affect only their respective notifier classes.
- Changes in data shape affect only the corresponding model (`Student`, `Post`).

---

## Open/Closed Principle (OCP)

Theory (what/why):
- Software entities should be open for extension but closed for modification.
- New features should be added by adding new code, not by editing stable code.

Implementation in this project (how):
- The abstraction `Notifier` defines the notification contract.
- New channels are added by creating new classes that implement `Notifier`:
	- `EmailNotifier`, `SMSNotifier`, `PushNotifier` were added without modifying `Forum`.
- `CompositeNotifier` extends behavior by composition — broadcasts a message to multiple `Notifier` implementations without changing `Forum` or the other notifiers.

Result:
- Adding a new channel (e.g., `SlackNotifier`) requires only a new class; no edits in `Forum`.

---

## Dependency Inversion Principle (DIP)

Theory (what/why):
- High-level modules should depend on abstractions, not concrete implementations.
- Details (implementations) depend on abstractions, enabling swapping and testability.

Implementation in this project (how):
- `Forum` depends on the `Notifier` abstraction, not on any concrete notifier.
- In `main.py`, a concrete notifier (or a composition of them) is injected:
	- `forum = Forum(CompositeNotifier([EmailNotifier(), SMSNotifier(), PushNotifier()]))`
- `CompositeNotifier` itself depends only on the `Notifier` abstraction for its children.

Result:
- We can switch from `EmailNotifier` to `SMSNotifier`, `PushNotifier`, `NullNotifier`, or a `CompositeNotifier` without any changes in `Forum`.
- Improves decoupling and makes the system easier to test.

---

## Small Project Map

- `models.py`
	- `Student` (SRP)
	- `Post` (SRP)
- `notifiers.py`
	- `Notifier` (DIP, OCP)
	- `EmailNotifier`, `SMSNotifier`, `PushNotifier` (SRP, OCP)
	- `NullNotifier` (SRP, DIP)
	- `CompositeNotifier` (DIP, OCP)
- `main.py`
	- `Forum` (SRP, DIP, OCP): manages posts, depends on `Notifier`, unaffected by new channels
	- `main()` composes dependencies and runs a short demo

---

## Conclusion

This simple forum demonstrates three SOLID principles:
- SRP keeps each class focused and easier to evolve.
- OCP enables new notification channels via extension, not modification.
- DIP decouples high-level logic (`Forum`) from low-level details (concrete notifiers), enabling easy swapping, composition, and testing.

