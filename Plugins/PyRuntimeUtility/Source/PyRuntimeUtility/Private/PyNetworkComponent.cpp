// Fill out your copyright notice in the Description page of Project Settings.


#include "PyNetworkComponent.h"
#include "SocketSubsystem.h"
#include "Interfaces/IPv4/IPv4Address.h"
#include "IPAddress.h"
#include "Sockets.h"
#include "HAL/RunnableThread.h"
#include "Async/Async.h"
#include <string>
#include "Logging/MessageLog.h"
#include "HAL/UnrealMemory.h"
//#include "TcpSocketSettings.h"




// Sets default values
APyNetworkComponent::APyNetworkComponent()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;

}

// Called when the game starts or when spawned
void APyNetworkComponent::BeginPlay()
{
	Super::BeginPlay();
	
}

// Called every frame
void APyNetworkComponent::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

}

