// Copyright Discord, Inc. All Rights Reserved.

#include "DiscordLocalPlayerSubsystem.h"

void UDiscordLocalPlayerSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Client = NewObject<UDiscordClient>();
    Client->Init();
    Client->SetStatusChangedCallback(FDiscordClientOnStatusChanged::CreateWeakLambda(
      this, [this](EDiscordClientStatus Status, EDiscordClientError Error, int32 ErrorDetail) {
          OnStatusChanged.Broadcast(Status, Error, ErrorDetail);
      }));
    Client->SetActivityInviteCreatedCallback(FDiscordClientActivityInviteCallback::CreateWeakLambda(
      this, [this](UDiscordActivityInvite* Invite) { OnActivityInvite.Broadcast(Invite); }));
    Client->SetActivityJoinCallback(FDiscordClientActivityJoinCallback::CreateWeakLambda(
      this, [this](FString Secret) { OnActivityJoin.Broadcast(Secret); }));
    Client->SetLobbyCreatedCallback(FDiscordClientLobbyCreatedCallback::CreateWeakLambda(
      this, [this](FDiscordUniqueID LobbyId) { OnLobbyCreated.Broadcast(LobbyId); }));
    Client->SetLobbyUpdatedCallback(FDiscordClientLobbyUpdatedCallback::CreateWeakLambda(
      this, [this](FDiscordUniqueID LobbyId) { OnLobbyUpdated.Broadcast(LobbyId); }));
    Client->SetLobbyDeletedCallback(FDiscordClientLobbyDeletedCallback::CreateWeakLambda(
      this, [this](FDiscordUniqueID LobbyId) { OnLobbyDeleted.Broadcast(LobbyId); }));
    Client->SetLobbyMemberAddedCallback(FDiscordClientLobbyMemberAddedCallback::CreateWeakLambda(
      this, [this](FDiscordUniqueID LobbyId, FDiscordUniqueID UserId) {
          OnLobbyMemberAdded.Broadcast(LobbyId, UserId);
      }));
    Client->SetLobbyMemberUpdatedCallback(
      FDiscordClientLobbyMemberUpdatedCallback::CreateWeakLambda(
        this, [this](FDiscordUniqueID LobbyId, FDiscordUniqueID UserId) {
            OnLobbyMemberUpdated.Broadcast(LobbyId, UserId);
        }));
    Client->SetLobbyMemberRemovedCallback(
      FDiscordClientLobbyMemberRemovedCallback::CreateWeakLambda(
        this, [this](FDiscordUniqueID LobbyId, FDiscordUniqueID UserId) {
            OnLobbyMemberRemoved.Broadcast(LobbyId, UserId);
        }));
    Client->SetMessageCreatedCallback(FDiscordClientMessageCreatedCallback::CreateWeakLambda(
      this, [this](FDiscordUniqueID MessageId) { OnMessageCreated.Broadcast(MessageId); }));
    Client->SetMessageDeletedCallback(FDiscordClientMessageDeletedCallback::CreateWeakLambda(
      this, [this](FDiscordUniqueID MessageId, FDiscordUniqueID ChannelId) {
          OnMessageDeleted.Broadcast(MessageId, ChannelId);
      }));
    Client->SetMessageUpdatedCallback(FDiscordClientMessageUpdatedCallback::CreateWeakLambda(
      this, [this](FDiscordUniqueID MessageId) { OnMessageUpdated.Broadcast(MessageId); }));
    Client->SetNoAudioInputCallback(FDiscordClientNoAudioInputCallback::CreateWeakLambda(
      this, [this](bool InputDetected) { OnNoAudioInput.Broadcast(InputDetected); }));
    Client->SetRelationshipCreatedCallback(
      FDiscordClientRelationshipCreatedCallback::CreateWeakLambda(
        this, [this](FDiscordUniqueID UserId, bool isDiscordRelationship) {
            OnRelationshipCreated.Broadcast(UserId, isDiscordRelationship);
        }));
    Client->SetRelationshipDeletedCallback(
      FDiscordClientRelationshipDeletedCallback::CreateWeakLambda(
        this, [this](FDiscordUniqueID UserId, bool isDiscordRelationship) {
            OnRelationshipDeleted.Broadcast(UserId, isDiscordRelationship);
        }));
    Client->SetUserUpdatedCallback(FDiscordClientUserUpdatedCallback::CreateWeakLambda(
      this, [this](FDiscordUniqueID UserId) { OnUserUpdated.Broadcast(UserId); }));

    TickerHandle = FTSBackgroundableTicker::GetCoreTicker().AddTicker(
      FTickerDelegate::CreateUObject(this, &UDiscordLocalPlayerSubsystem::RunDiscordCallbacks),
      0.0f);
}

void UDiscordLocalPlayerSubsystem::Deinitialize()
{
    if (TickerHandle.IsValid()) {
        FTSBackgroundableTicker::GetCoreTicker().RemoveTicker(TickerHandle);
        TickerHandle.Reset();
    }

    Disconnect();
}

bool UDiscordLocalPlayerSubsystem::ShouldCreateSubsystem(UObject* Outer) const
{
#if DISCORD_PARTNER_SDK_STUB
    return false;
#else
    return true;
#endif
}

void UDiscordLocalPlayerSubsystem::Connect(FString const& Token)
{
    Client->Disconnect();
    Client->UpdateToken(EDiscordAuthorizationTokenType::Bearer,
                        Token,
                        FDiscordClientUpdateTokenCallback::CreateWeakLambda(
                          this, [this](auto) { Client->Connect(); }));
}

void UDiscordLocalPlayerSubsystem::Disconnect()
{
    Client->Disconnect();
}

bool UDiscordLocalPlayerSubsystem::RunDiscordCallbacks(float DeltaTime)
{
#if !DISCORD_PARTNER_SDK_STUB
    Discord_RunCallbacks();
#endif
    return true;
}
