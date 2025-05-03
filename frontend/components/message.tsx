'use client';

import type { UIMessage } from 'ai';
import cx from 'classnames';
import { AnimatePresence, motion } from 'framer-motion';
import { Dispatch, memo, SetStateAction, useState } from 'react';
import type { Vote } from '@/lib/db/schema';
import { DocumentToolCall, DocumentToolResult } from './document';
import { BotIcon, PencilEditIcon } from './icons';
import { Markdown } from './markdown';
import { MessageActions } from './message-actions';
import { PreviewAttachment } from './preview-attachment';
import { Weather } from './weather';
import equal from 'fast-deep-equal';
import { cn } from '@/lib/utils';
import { Button } from './ui/button';
import { Tooltip, TooltipContent, TooltipTrigger } from './ui/tooltip';
import { MessageEditor } from './message-editor';
import { DocumentPreview } from './document-preview';
import { MessageReasoning } from './message-reasoning';
import type { UseChatHelpers } from '@ai-sdk/react';
import { CreatePayment, GetPayment, ListPayments } from './bunq/payments';
import {
  CreateRequestInquiry,
  GetRequestInquiry,
  ListRequestInquiries,
} from './bunq/request-inquiries';

const PurePreviewMessage = ({
  chatId,
  message,
  vote,
  isLoading,
  setMessages,
  reload,
  isReadonly,
  requiresScrollPadding,
}: {
  chatId: string;
  message: UIMessage;
  vote: Vote | undefined;
  isLoading: boolean;
  setMessages: UseChatHelpers['setMessages'];
  reload: UseChatHelpers['reload'];
  isReadonly: boolean;
  requiresScrollPadding: boolean;
}) => {
  const [mode, setMode] = useState<'view' | 'edit'>('view');

  return (
    <AnimatePresence>
      <motion.div
        data-testid={`message-${message.role}`}
        className="w-full mx-auto max-w-3xl px-4 group/message"
        initial={{ y: 5, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        data-role={message.role}
      >
        <div
          className={cn(
            'flex gap-4 w-full group-data-[role=user]/message:ml-auto group-data-[role=user]/message:max-w-2xl',
            {
              'w-full': mode === 'edit',
              'group-data-[role=user]/message:w-fit': mode !== 'edit',
            },
          )}
        >
          {message.role === 'assistant' && (
            <div className="size-8 flex items-center rounded-full justify-center ring-1 shrink-0 ring-border bg-background">
              <div className="translate-y-px">
                <BotIcon />
              </div>
            </div>
          )}

          <div
            className={cn('flex flex-col gap-4 w-full', {
              'min-h-96': message.role === 'assistant' && requiresScrollPadding,
            })}
          >
            {message.experimental_attachments &&
              message.experimental_attachments.length > 0 && (
                <div
                  data-testid={`message-attachments`}
                  className="flex flex-row justify-end gap-2"
                >
                  {message.experimental_attachments.map((attachment) => (
                    <PreviewAttachment
                      key={attachment.url}
                      attachment={attachment}
                    />
                  ))}
                </div>
              )}

            {message.parts?.map((part, index) => (
              <MessagePart
                key={`${message.id}-${index}`}
                index={index}
                part={part}
                message={message}
                isLoading={isLoading}
                mode={mode}
                isReadonly={isReadonly}
                setMode={setMode}
                setMessages={setMessages}
                reload={reload}
              />
            ))}

            {!isReadonly && (
              <MessageActions
                key={`action-${message.id}`}
                chatId={chatId}
                message={message}
                vote={vote}
                isLoading={isLoading}
              />
            )}
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
};

export const MessagePart = ({
  index,
  part,
  message,
  isLoading,
  mode,
  isReadonly,
  setMode,
  setMessages,
  reload,
}: {
  index: number;
  part: UIMessage['parts'][number];
  message: UIMessage;
  isLoading: boolean;
  mode: 'view' | 'edit';
  isReadonly: boolean;
  setMode: Dispatch<SetStateAction<'view' | 'edit'>>;
  setMessages: UseChatHelpers['setMessages'];
  reload: UseChatHelpers['reload'];
}) => {
  const { type } = part;
  const key = `message-${message.id}-part-${index}`;

  if (type === 'reasoning') {
    return (
      <MessageReasoning
        key={key}
        isLoading={isLoading}
        reasoning={part.reasoning}
      />
    );
  }

  if (type === 'text') {
    if (mode === 'view') {
      return (
        <div key={key} className="flex flex-row gap-2 items-start">
          {message.role === 'user' && !isReadonly && (
            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  data-testid="message-edit-button"
                  variant="ghost"
                  className="px-2 h-fit rounded-full text-muted-foreground opacity-0 group-hover/message:opacity-100"
                  onClick={() => {
                    setMode('edit');
                  }}
                >
                  <PencilEditIcon />
                </Button>
              </TooltipTrigger>
              <TooltipContent>Edit message</TooltipContent>
            </Tooltip>
          )}

          <div
            data-testid="message-content"
            className={cn('flex flex-col gap-4', {
              'bg-primary text-primary-foreground px-3 py-2 rounded-xl':
                message.role === 'user',
            })}
          >
            <Markdown>{part.text}</Markdown>
          </div>
        </div>
      );
    }

    if (mode === 'edit') {
      return (
        <div key={key} className="flex flex-row gap-2 items-start">
          <div className="size-8" />

          <MessageEditor
            key={message.id}
            message={message}
            setMode={setMode}
            setMessages={setMessages}
            reload={reload}
          />
        </div>
      );
    }
  }

  if (type === 'tool-invocation') {
    const { toolInvocation } = part;
    const { toolName, toolCallId, state } = toolInvocation;

    if (state === 'call') {
      const { args } = toolInvocation;

      return (
        <div
          key={toolCallId}
          className={cx({
            skeleton: ['getWeather'].includes(toolName),
          })}
        >
          {toolName === 'getWeather' ? (
            <Weather />
          ) : toolName === 'createDocument' ? (
            <DocumentPreview isReadonly={isReadonly} args={args} />
          ) : toolName === 'updateDocument' ? (
            <DocumentToolCall
              type="update"
              args={args}
              isReadonly={isReadonly}
            />
          ) : toolName === 'requestSuggestions' ? (
            <DocumentToolCall
              type="request-suggestions"
              args={args}
              isReadonly={isReadonly}
            />
          ) : toolName === 'createPayment' ? (
            <CreatePayment args={args} isReadonly={isReadonly} />
          ) : toolName === 'getPayment' ? (
            <GetPayment args={args} isReadonly={isReadonly} />
          ) : toolName === 'listPayments' ? (
            <ListPayments args={args} isReadonly={isReadonly} />
          ) : toolName === 'createRequestInquiry' ? (
            <CreateRequestInquiry args={args} isReadonly={isReadonly} />
          ) : toolName === 'getRequestInquiry' ? (
            <GetRequestInquiry args={args} isReadonly={isReadonly} />
          ) : toolName === 'listRequestInquiries' ? (
            <ListRequestInquiries args={args} isReadonly={isReadonly} />
          ) : (
            <details open={false}>
              <summary>
                <span className="text-muted-foreground ">
                  Calling
                  <span className="font-mono text-sm"> {toolName}()</span>
                </span>
              </summary>
            </details>
          )}
        </div>
      );
    }

    if (state === 'result') {
      const { result } = toolInvocation;

      return (
        <div key={toolCallId}>
          {toolName === 'getWeather' ? (
            <Weather weatherAtLocation={result} />
          ) : toolName === 'createDocument' ? (
            <DocumentPreview isReadonly={isReadonly} result={result} />
          ) : toolName === 'updateDocument' ? (
            <DocumentToolResult
              type="update"
              result={result}
              isReadonly={isReadonly}
            />
          ) : toolName === 'requestSuggestions' ? (
            <DocumentToolResult
              type="request-suggestions"
              result={result}
              isReadonly={isReadonly}
            />
          ) : toolName === 'createPayment' ? (
            <CreatePayment result={result} isReadonly={isReadonly} />
          ) : toolName === 'getPayment' ? (
            <GetPayment result={result} isReadonly={isReadonly} />
          ) : toolName === 'listPayments' ? (
            <ListPayments result={result} isReadonly={isReadonly} />
          ) : toolName === 'createRequestInquiry' ? (
            <CreateRequestInquiry result={result} isReadonly={isReadonly} />
          ) : toolName === 'getRequestInquiry' ? (
            <GetRequestInquiry result={result} isReadonly={isReadonly} />
          ) : toolName === 'listRequestInquiries' ? (
            <ListRequestInquiries result={result} isReadonly={isReadonly} />
          ) : (
            <details>
              <summary>
                <span className="text-muted-foreground">
                  Called
                  <span className="font-mono text-sm"> {toolName}()</span>
                </span>
              </summary>
              <pre className="text-xs bg-muted rounded-md p-4 overflow-x-scroll">
                {JSON.stringify(result, null, 2)}
              </pre>
            </details>
          )}
        </div>
      );
    }
  }
};

export const PreviewMessage = memo(
  PurePreviewMessage,
  (prevProps, nextProps) => {
    if (prevProps.isLoading !== nextProps.isLoading) return false;
    if (prevProps.message.id !== nextProps.message.id) return false;
    if (prevProps.requiresScrollPadding !== nextProps.requiresScrollPadding)
      return false;
    if (!equal(prevProps.message.parts, nextProps.message.parts)) return false;
    if (!equal(prevProps.vote, nextProps.vote)) return false;

    return true;
  },
);

export const ThinkingMessage = () => {
  const role = 'assistant';

  return (
    <motion.div
      data-testid="message-assistant-loading"
      className="w-full mx-auto max-w-3xl px-4 group/message min-h-96"
      initial={{ y: 5, opacity: 0 }}
      animate={{ y: 0, opacity: 1, transition: { delay: 1 } }}
      data-role={role}
    >
      <div
        className={cx(
          'flex gap-4 group-data-[role=user]/message:px-3 w-full group-data-[role=user]/message:w-fit group-data-[role=user]/message:ml-auto group-data-[role=user]/message:max-w-2xl group-data-[role=user]/message:py-2 rounded-xl',
          {
            'group-data-[role=user]/message:bg-muted': true,
          },
        )}
      >
        <div className="size-8 flex items-center rounded-full justify-center ring-1 shrink-0 ring-border">
          <BotIcon />
        </div>

        <div className="flex flex-col gap-2 w-full">
          <div className="flex flex-col gap-4 text-muted-foreground">
            Hmm...
          </div>
        </div>
      </div>
    </motion.div>
  );
};
