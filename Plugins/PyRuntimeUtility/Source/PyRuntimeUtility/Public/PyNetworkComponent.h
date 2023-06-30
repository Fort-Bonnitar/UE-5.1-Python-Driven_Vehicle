// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PyNetworkComponent.generated.h"
#include "HAL/Runnable.h"
#include "HAL/ThreadSafeBool.h"
#include "Containers/Queue.h"
#include "UObject/WeakObjectPtrTemplates.h"


DECLARE_DYNAMIC_DELEGATE_OneParam(FPyNetworkDisconnectDelegate, int32, ConnectionId);
DECLARE_DYNAMIC_DELEGATE_OneParam(FPyNetworkConnectDelegate, int32, ConnectionId);
DECLARE_DYNAMIC_DELEGATE_TwoParams(FPyNetworkReceivedMessageDelegate, int32, ConnectionId, UPARAM(ref) TArray<uint8>&, Message);

UCLASS(Blueprintable, BlueprintType)
class PYRUNTIMEUTILITY_API APyNetworkComponent : public AActor
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	APyNetworkComponent();

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

public:	
	// Called every frame
	virtual void Tick(float DeltaTime) override;

	/* Returns the ID of the new connection. */
	UFUNCTION(BlueprintCallable, Category = "PythonRuntimeConnection")
		void Connect(const FString& ipAddress, int32 port,
			const FPyNetworkDisconnectDelegate& OnDisconnected, const FPyNetworkConnectDelegate& OnConnected,
			const FPyNetworkReceivedMessageDelegate& OnMessageReceived, int32& ConnectionId);


	/* Disconnect from connection ID. */
	UFUNCTION(BlueprintCallable, Category = "PythonRuntimeConnection")
		void Disconnect(int32 ConnectionId);


	/* False means we're not connected to socket and the data wasn't sent. "True" doesn't guarantee that it was successfully sent,
	only that we were still connected when we initiating the sending process. */
	UFUNCTION(BlueprintCallable, Category = "PythonRuntimeConnection") // use meta to set first default param to 0
		bool SendData(int32 ConnectionId, TArray<uint8> DataToSend);

	//UFUNCTION(Category = ""PythonRuntimeConnection")	
	void ExecuteOnConnected(int32 WorkerId, TWeakObjectPtr<APyNetworkComponent> thisObj);

	//UFUNCTION(Category = "PythonRuntimeConnection")
	void ExecuteOnDisconnected(int32 WorkerId, TWeakObjectPtr<APyNetworkComponent> thisObj);

	//UFUNCTION(Category = "PythonRuntimeConnection")
	void ExecuteOnMessageReceived(int32 ConnectionId, TWeakObjectPtr<APyNetworkComponent> thisObj);

	UFUNCTION(BlueprintPure, meta = (DisplayName = "Append Bytes", CommutativeAssociativeBinaryOperator = "true"), Category = "PythonRuntimeConnection")
		static TArray<uint8> Concat_BytesBytes(TArray<uint8> A, TArray<uint8> B);

	/** Converts an integer to an array of bytes */
	UFUNCTION(BlueprintPure, meta = (DisplayName = "Int To Bytes", CompactNodeTitle = "->", Keywords = "cast convert", BlueprintAutocast), Category = "PythonRuntimeConnection")
		static TArray<uint8> Conv_IntToBytes(int32 InInt);

	/** Converts a string to an array of bytes */
	UFUNCTION(BlueprintPure, meta = (DisplayName = "String To Bytes", CompactNodeTitle = "->", Keywords = "cast convert", BlueprintAutocast), Category = "PythonRuntimeConnection")
		static TArray<uint8> Conv_StringToBytes(const FString& InStr);


	/** Converts a float to an array of bytes */
	UFUNCTION(BlueprintPure, meta = (DisplayName = "Float To Bytes", CompactNodeTitle = "->", Keywords = "cast convert", BlueprintAutocast), Category = "PythonRuntimeConnection")
		static TArray<uint8> Conv_FloatToBytes(float InFloat);

	/** Converts a byte to an array of bytes */
	UFUNCTION(BlueprintPure, meta = (DisplayName = "Byte To Bytes", CompactNodeTitle = "->", Keywords = "cast convert", BlueprintAutocast), Category = "PythonRuntimeConnection")
		static TArray<uint8> Conv_ByteToBytes(uint8 InByte);

	UFUNCTION(BlueprintCallable, meta = (DisplayName = "Read Int", Keywords = "read int"), Category = "PythonRuntimeConnection")
		static int32 Message_ReadInt(UPARAM(ref) TArray<uint8>& Message);


	UFUNCTION(BlueprintCallable, meta = (DisplayName = "Read Byte", Keywords = "read byte int8 uint8"), Category = "PythonRuntimeConnection")
		static uint8 Message_ReadByte(UPARAM(ref) TArray<uint8>& Message);

	UFUNCTION(BlueprintCallable, meta = (DisplayName = "Read Bytes", Keywords = "read bytes"), Category = "PythonRuntimeConnection")
		static bool Message_ReadBytes(int32 NumBytes, UPARAM(ref) TArray<uint8>& Message, TArray<uint8>& ReturnArray);

	UFUNCTION(BlueprintCallable, meta = (DisplayName = "Read Float", Keywords = "read float"), Category = "PythonRuntimeConnection")
		static float Message_ReadFloat(UPARAM(ref) TArray<uint8>& Message);

	UFUNCTION(BlueprintCallable, meta = (DisplayName = "Read String", Keywords = "read string"), Category = "PythonRuntimeConnection")
		static FString Message_ReadString(UPARAM(ref) TArray<uint8>& Message, int32 StringLength);

	UFUNCTION(BlueprintCallable, BlueprintPure, Category = "PythonRuntimeConnection")
		bool isConnected(int32 ConnectionId);

	/* Used by the separate threads to print to console on the main thread. */
	static void PrintToConsole(FString Str, bool Error);

	/* Buffer size in bytes. Currently not used. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PythonRuntimeConnection")
		int32 SendBufferSize = 16384;

	/* Buffer size in bytes. It's set only when creating a socket, never afterwards. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PythonRuntimeConnection")
		int32 ReceiveBufferSize = 16384;

	/* Time between ticks. Please account for the fact that it takes 1ms to wake up on a modern PC, so 0.01f would effectively be 0.011f */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PythonRuntimeConnection")
		float TimeBetweenTicks = 0.008f;

private:
	TMap<int32, TSharedRef<class FPythonRuntimeConnectionWorker>> PythonConnectionWorkers;

	FPyNetworkComponentDisconnectDelegate DisconnectedDelegate;
	FPyNetworkComponentConnectDelegate ConnectedDelegate;
	FPyNetworkComponentReceivedMessageDelegate MessageReceivedDelegate;
};


private:
	class FSocket* Socket = nullptr;
	FString ipAddress;
	int port;
	TWeakObjectPtr<APyNetworkComponent> ThreadSpawnerActor;
	int32 id;
	int32 RecvBufferSize;
	int32 ActualRecvBufferSize;
	int32 SendBufferSize;
	int32 ActualSendBufferSize;
	float TimeBetweenTicks;
	FThreadSafeBool bConnected = false;

	// SPSC = single producer, single consumer.
	TQueue<TArray<uint8>, EQueueMode::Spsc> Inbox; // Messages we read from socket and send to main thread. Runner thread is producer, main thread is consumer.
	TQueue<TArray<uint8>, EQueueMode::Spsc> Outbox; // Messages to send to socket from main thread. Main thread is producer, runner thread is consumer.



public:

	//Constructor / Destructor
	FPythonRuntimeConnectionWorker(FString inIp, const int32 inPort, TWeakObjectPtr<APyNetworkComponent> InOwner, int32 inId, int32 inRecvBufferSize, int32 inSendBufferSize, float inTimeBetweenTicks);
	virtual ~FPythonRuntime();

	/*  Starts processing of the connection. Needs to be called immediately after construction	 */
	void Start();

	/* Adds a message to the outgoing message queue */
	void AddToOutbox(TArray<uint8> Message);

	/* Reads a message from the inbox queue */
	TArray<uint8> ReadFromInbox();

	// Begin FRunnable interface.
	virtual bool Init() override;
	virtual uint32 Run() override;
	virtual void Stop() override;
	virtual void Exit() override;
	// End FRunnable interface	

	/** Shuts down the thread */
	void SocketShutdown();

	/* Getter for bConnected */
	bool isConnected();

private:
	/* Blocking send */
	bool BlockingSend(const uint8* Data, int32 BytesToSend);

	/** thread should continue running */
	FThreadSafeBool bRun = false;

	/** Critical section preventing multiple threads from sending simultaneously */
	//FCriticalSection SendCriticalSection;
};
